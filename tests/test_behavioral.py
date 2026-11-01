"""Opt-in live rehearsal of the actual module agents and persisted graph.

RUN_BEHAVIORAL=1 uv run pytest tests/test_behavioral.py -v
Requires configured AuraDB (or CI's disposable Neo4j) and OpenAI. Uses temporary
SQLite data and unique conversation IDs. Never wipes the participant's graph.
NAMS lifecycle checks require a separate configured-workspace rehearsal; offline
request choreography is covered by test_nams_workflows.py.
"""

from __future__ import annotations

import os
from uuid import uuid4

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
    settings = get_settings()
    if not (settings.openai_api_key and settings.neo4j_uri and settings.neo4j_password):
        pytest.skip("Configure OpenAI and Neo4j credentials to rehearse live modules")
    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    return settings.model_copy(update={"data_dir": tmp_path})


async def test_module_1_live_business_tools_without_memory(live_settings):
    async with open_agent(1, live_settings) as chat:
        result = await chat.chat(
            "Use lookup_account for maya.chen@northwind.example and tell me her plan.",
            f"rehearsal-m1-{uuid4().hex}",
        )
        assert any(call["name"] == "lookup_account" for call in result["tool_calls"])
        assert "pro" in result["reply"].lower()
        assert not result["context"]["used_memory"]
        assert chat.memory is None


async def test_module_2_live_restart_and_context(live_settings):
    session = f"rehearsal-m2-{uuid4().hex}"
    phrase = f"amber-{uuid4().hex[:10]}"
    async with open_agent(2, live_settings) as chat:
        await chat.chat(f"Remember my verification phrase: {phrase}.", session)
    async with open_agent(2, live_settings) as restarted:
        context = await restarted.memory.get_context("verification phrase", session_id=session)
        assert phrase in context
        result = await restarted.chat("What is my exact verification phrase?", session)
        assert phrase in result["reply"]
        assert "short_term" in result["context"]["summary"]
        entities = await restarted.memory.query.cypher(
            "MATCH (c:Conversation {session_id: $session})-[:HAS_MESSAGE]->(:Message)"
            "-[:MENTIONS]->(e:Entity) RETURN count(e) AS n",
            {"session": session},
        )
        assert entities[0]["n"] == 0


async def test_module_3_live_extraction_grounding_and_preferences(live_settings):
    session = f"rehearsal-m3-{uuid4().hex}"
    preference_marker = f"support-ref-{uuid4().hex[:10]}"
    async with open_agent(3, live_settings, ontology="acme_cloud") as chat:
        result = await chat.chat(
            "I'm Maya Chen at Northwind Robotics on the Pro plan. I use Acme Cloud Compute. "
            "Please save my support preference: email rather than phone. "
            f"Use the exact preference category '{preference_marker}'.",
            session,
        )
        entities = await chat.memory.query.cypher(
            "MATCH (c:Conversation {session_id: $session})-[:HAS_MESSAGE]->(:Message)"
            "-[:MENTIONS]->(e:Entity) RETURN DISTINCT e.name AS name, labels(e) AS labels, "
            "e.email AS email, e.signup_date AS signup_date, e.hydrated_from AS source",
            {"session": session},
        )
        customers = [e for e in entities if "Customer" in e["labels"]]
        assert customers, entities
        assert any(e["email"] == "maya.chen@northwind.example" for e in customers)
        assert any(e["signup_date"] == "2025-03-14" for e in customers)
        assert all(e["source"] == "sqlite:customers" for e in customers)
        saved = [c for c in result["tool_calls"] if c["name"] == "save_preference"]
        assert saved, result
        # A unique category prevents the library from deduplicating this test's
        # preference onto an earlier run's globally stored email preference.
        details = saved[0]["input"]
        assert details["category"] == preference_marker, saved
        query = f"{details['category']}: {details['preference']}"
        if details.get("context"):
            query += f" ({details['context']})"
        prefs = await chat.memory.long_term.search_preferences(
            query, category=preference_marker, limit=10
        )
        assert any(
            p.category == preference_marker and "email" in p.preference.lower()
            for p in prefs
        )


@pytest.mark.parametrize("number", [4, 5])
async def test_reasoning_modules_live_trace_outcomes_and_retrieval(number, live_settings):
    session = f"rehearsal-m{number}-{uuid4().hex}"
    rejected_task = f"Attempt a $400 spot-capacity refund (rehearsal {session})"
    async with open_agent(number, live_settings) as chat:
        first = await chat.chat(
            "Maya Chen, maya.chen@northwind.example. Please issue a $49 refund for a duplicate "
            "Acme Cloud Compute charge. Look up my account and the refund policy first.",
            session,
        )
        assert any(
            c["name"] == "issue_refund" and c["output"]["status"] == "issued"
            for c in first["tool_calls"]
        )
        # Force the tool-rejection path deterministically; a real LLM may correctly
        # refuse the request before calling the tool. Recording still uses real Neo4j.
        turns = 0

        def over_limit(messages, info):
            nonlocal turns
            turns += 1
            if turns == 1:
                return ModelResponse(
                    parts=[
                        ToolCallPart(
                            "issue_refund",
                            {
                                "customer_email": "maya.chen@northwind.example",
                                "amount": 400,
                                "reason": "unused spot capacity",
                            },
                        )
                    ]
                )
            return ModelResponse(parts=[TextPart("Rejected above the policy limit; escalate.")])

        with chat.agent.override(model=FunctionModel(over_limit)):
            await chat.chat(rejected_task, session)
        traces = await chat.memory.query.cypher(
            "MATCH (t:ReasoningTrace {session_id: $session}) "
            "RETURN t.success AS success, t.outcome AS outcome",
            {"session": session},
        )
        assert any(t["success"] is True for t in traces), traces
        assert any(t["success"] is False for t in traces), traces
        recalled = await chat.memory.reasoning.get_similar_traces(
            rejected_task, success_only=False, limit=10
        )
        assert any(t.session_id == session and t.success is False for t in recalled)
    async with open_agent(number, live_settings, reasoning_retrieval=False) as control:
        reply = await control.chat(
            "Have you refunded an Acme Cloud duplicate charge?", session + "-off"
        )
        assert "reasoning" not in (reply["context"]["summary"] or "")
    async with open_agent(number, live_settings, reasoning_retrieval=True) as treatment:
        reply = await treatment.chat(
            "Have you refunded an Acme Cloud duplicate charge?", session + "-on"
        )
        assert "reasoning" in reply["context"]["summary"]


async def test_module_5_live_fresh_agent_with_fallback(live_settings):
    from module_5.app.fresh_agent import run_fresh_agent

    result = await run_fresh_agent(live_settings, mode="fallback")
    assert result["with_skill"]
    assert any(
        c["name"] == "issue_refund" and c["output"]["status"] == "issued"
        for c in result["tool_calls"]
    )
