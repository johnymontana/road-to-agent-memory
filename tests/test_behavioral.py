"""Opt-in live non-NAMS regression checks; missing credentials fail an opted-in run."""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import FunctionModel

from lib.settings import get_settings
from lib.workshop import open_agent

pytestmark = [
    pytest.mark.behavioral,
    pytest.mark.skipif(os.environ.get("RUN_BEHAVIORAL") != "1", reason="Opt-in live services"),
]


@pytest.fixture
def live_settings(tmp_path, monkeypatch):
    from scripts import seed_sqlite

    get_settings.cache_clear()
    s = get_settings()
    assert s.openai_api_key and s.neo4j_uri and s.neo4j_password, (
        "Opted-in live job requires OpenAI and Neo4j credentials"
    )
    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    return s.model_copy(update={"data_dir": tmp_path, "memory_namespace": "live-" + uuid4().hex})


def tool_model(name, args):
    calls = 0

    def answer(messages, info):
        nonlocal calls
        calls += 1
        return (
            ModelResponse(parts=[ToolCallPart(name, args)])
            if calls == 1
            else ModelResponse(parts=[TextPart("Completed")])
        )

    return FunctionModel(answer)


async def graph_http(chat, settings, session, monkeypatch):
    from lib import app_factory

    monkeypatch.setattr(app_factory, "get_settings", lambda: settings)

    @asynccontextmanager
    async def factory(settings):
        yield chat

    app = app_factory.create_app(factory, title="Live lesson check")
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as http,
    ):
        graphs = {}
        for layer in ("all", "short_term", "long_term", "reasoning"):
            response = await http.get("/api/graph", params={"session_id": session, "layer": layer})
            assert response.status_code == 200
            g = response.json()
            ids = {n["id"] for n in g["nodes"]}
            assert all(r["from"] in ids and r["to"] in ids for r in g["relationships"])
            assert not any("embedding" in k.lower() for n in g["nodes"] for k in n["properties"])
            graphs[layer] = g
        return graphs


async def test_module_1_live_sql_and_stateless_control(live_settings):
    async with open_agent(1, live_settings) as chat:
        result = await chat.chat("Look up maya.chen@northwind.example and tell me her plan.", "m1")
        assert any(c["name"] == "lookup_account" for c in result["tool_calls"])
        assert "Pro" in result["reply"] and result["execution_status"] == "succeeded"
        assert chat.memory is None


async def test_module_2_restart_latest_history_and_http_graph(live_settings, monkeypatch):
    phrase = "violet-" + uuid4().hex[:8]
    async with open_agent(2, live_settings) as first:
        result = await first.chat(f"Remember my unique phrase {phrase}.", "restart")
        session = result["session_id"]
    async with open_agent(2, live_settings) as second:
        result = await second.chat("What unique phrase did I give you?", "restart")
        assert phrase in result["reply"]
        assert any(e["path"] == "recent_conversation" for e in result["context"]["evidence"])
        graphs = await graph_http(second, live_settings, session, monkeypatch)
        assert len(graphs["short_term"]["nodes"]) >= 5
        from module_2.app.context import recent_messages

        for i in range(12):
            await second.memory.short_term.add_message(
                session,
                "user",
                f"Window marker {i}",
                extract_entities=False,
                generate_embedding=False,
            )
        rows = await recent_messages(second.memory, session)
        assert (
            len(rows) == 10
            and rows[-1]["content"] == "Window marker 11"
            and rows[0]["content"] == "Window marker 2"
        )


async def test_module_3_grounding_and_two_customer_preferences(live_settings, monkeypatch):
    async with open_agent(3, live_settings) as chat:
        result = await chat.chat(
            "I am Maya Chen at Northwind Robotics. What is my grounded signup date and email?",
            "profile",
            account_email="maya.chen@northwind.example",
        )
        assert result["execution_status"] == "succeeded", result
        assert result["context"]["hydrated"], result
        facts = await chat.memory.query.cypher(
            'MATCH (e:Entity {name:"Maya Chen"}) RETURN e.email AS '
            "email,e.signup_date AS signup_date"
        )
        assert (
            facts[0]["email"] == "maya.chen@northwind.example"
            and facts[0]["signup_date"] == "2025-03-14"
        )
        for email, preference in [
            ("maya.chen@northwind.example", "Email only"),
            ("dana.w@contoso.example", "Phone only"),
        ]:
            model = tool_model(
                "save_preference",
                {"category": "contact", "preference": preference, "context": "Workshop support"},
            )
            with chat.agent.override(model=model):
                saved = await chat.chat(
                    "Save my explicit contact preference.", "preferences", account_email=email
                )
            receipt = json.loads(saved["tool_calls"][0]["output"])
            assert receipt["preference"] == preference and receipt["context"] == "Workshop support"
        from module_3.app.context import search_preferences

        maya = await search_preferences(
            chat.memory, "maya.chen@northwind.example", live_settings.memory_namespace
        )
        dana = await search_preferences(
            chat.memory, "dana.w@contoso.example", live_settings.memory_namespace
        )
        assert maya[0]["preference"] == "Email only" and dana[0]["preference"] == "Phone only"
        graph = await graph_http(chat, live_settings, result["session_id"], monkeypatch)
        shown_ids = {
            n["properties"]["id"]
            for n in graph["long_term"]["nodes"]
            if "Preference" in n["labels"]
        }
        assert maya[0]["id"] in shown_ids and dana[0]["id"] not in shown_ids
        assert "HAS_PREFERENCE" in {r["type"] for r in graph["long_term"]["relationships"]}


async def test_module_4_receipts_guards_provenance_and_failure(live_settings, monkeypatch):
    from lib.db import connect

    async with open_agent(4, live_settings) as chat:
        scope = {
            "account_email": "maya.chen@northwind.example",
            "incident_id": "maya-duplicate-compute",
            "authorize_refund": True,
        }
        result = await chat.chat(
            "Refund my duplicate $49 Compute charge.", "action", request_id="live-retry", **scope
        )
        assert result["business_status"] == "issued", result
        assert not result["warnings"], result
        retry = await chat.chat(
            "Refund my duplicate $49 Compute charge.", "action", request_id="live-retry", **scope
        )
        assert retry == result
        with connect(live_settings.db_path) as db:
            assert db.execute("SELECT count(*) FROM refunds").fetchone()[0] == 1
        model = tool_model(
            "issue_refund",
            {"customer_email": "dana.w@contoso.example", "amount": 400, "reason": "wrong identity"},
        )
        with chat.agent.override(model=model):
            wrong = await chat.chat(
                "Refund ops lead Pro $400.",
                "wrong",
                account_email="ravi.shah@northwind.example",
                incident_id="ravi-spot-capacity",
                authorize_refund=True,
            )
        assert wrong["business_status"] == "rejected_wrong_account", wrong
        with connect(live_settings.db_path) as db:
            assert db.execute("SELECT count(*) FROM refunds").fetchone()[0] == 1
        graphs = await graph_http(chat, live_settings, result["session_id"], monkeypatch)
        types = {r["type"] for r in graphs["all"]["relationships"]}
        assert {"INITIATED_BY", "TOUCHED", "USES_TOOL", "INSTANCE_OF"} <= types, types
        from module_4.app.reasoning import similar_executions

        examples, evidence = await similar_executions(
            chat.memory,
            "Refund duplicate $49 Compute charge",
            chat.embedder,
            live_settings.memory_namespace,
        )
        assert "executed_sql" in examples and result["reply"] in examples and evidence

        def fail(*args):
            raise RuntimeError("injected model failure")

        monkeypatch.setattr(
            "module_4.app.agent.hydrate_session_entities",
            AsyncMock(side_effect=RuntimeError("routing")),
        )
        with chat.agent.override(model=FunctionModel(fail)):
            failed = await chat.chat("No business action; demonstrate a model error.", "error")
        assert failed["execution_status"] == "failed" and any(
            w["phase"] == "hydration" for w in failed["warnings"]
        )
        traces = await chat.memory.query.cypher(
            (
                "MATCH (t:ReasoningTrace {session_id:$session}) RETURN t.outcome "
                "AS outcome,t.success AS success"
            ),
            {"session": failed["session_id"]},
        )
        assert (
            traces and traces[0]["success"] is False and "execution_status" in traces[0]["outcome"]
        )
