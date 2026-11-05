"""Exercise every lesson through real PydanticAI runs, with local memory adapters.

No external credentials or services are used. The same factories serve HTTP,
scenario playback, and eval; the tests verify observable stage behavior.
"""

from __future__ import annotations

import ast
import importlib
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import FunctionModel

from lib.settings import AppSettings
from lib.workshop import load_agent_module, open_agent

ROOT = Path(__file__).resolve().parents[1]
BUSINESS_TOOLS = {
    "lookup_account",
    "search_product_catalog",
    "fetch_policy",
    "check_service_status",
    "issue_refund",
}
MEMORY_TOOLS = {"search_memory", "save_preference", "recall_preferences"}


@pytest.fixture
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from scripts import seed_sqlite

    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    return AppSettings(
        _env_file=None,
        openai_api_key="test-key",
        neo4j_uri="bolt://localhost:7687",
        neo4j_password="testpassword",
        data_dir=tmp_path,
    )


class Memory:
    def __init__(self):
        self.events = []
        self.messages = []
        self.context_options = []
        self.short_term = SimpleNamespace(
            create_conversation=AsyncMock(side_effect=self.create),
            add_message=AsyncMock(side_effect=self.add),
            search_messages=AsyncMock(return_value=[]),
        )
        self.long_term = SimpleNamespace(
            search_entities=AsyncMock(return_value=[]),
            search_preferences=AsyncMock(return_value=[]),
            add_preference=AsyncMock(),
            get_preferences_for=AsyncMock(return_value=[]),
            add_entity=AsyncMock(
                return_value=(SimpleNamespace(id="00000000-0000-0000-0000-000000000001"), None)
            ),
        )
        self.query = SimpleNamespace(cypher=AsyncMock(side_effect=self.query_rows))
        self.trace = SimpleNamespace(
            id="trace-id",
            task="Prior refund procedure",
            outcome="Refund issued",
            success=True,
        )
        self.reasoning = SimpleNamespace(
            get_similar_traces=AsyncMock(return_value=[self.trace]),
            start_trace=AsyncMock(return_value=self.trace),
            add_step=AsyncMock(return_value=SimpleNamespace(id="step-id")),
            record_tool_call=AsyncMock(),
            link_trace_to_message=AsyncMock(),
            complete_trace=AsyncMock(return_value=self.trace),
        )

    async def query_rows(self, query, params):
        if "workshop:recent" in query:
            return [
                {"id": str(i), "role": role, "content": text}
                for i, (sid, role, text) in reversed(list(enumerate(self.messages)))
                if sid == params["session_id"]
            ][-10:]
        return []

    async def create(self, session_id):
        self.events.append(("conversation", session_id))

    async def add(self, session_id, role, content, **kwargs):
        self.events.append(("write", role))
        self.messages.append((session_id, role, content))
        from uuid import uuid4

        return SimpleNamespace(id=uuid4())

    async def get_context(self, message, *, session_id, **options):
        self.context_options.append(options)
        self.events.append(("retrieve", session_id))
        return "\n".join(text for sid, _, text in self.messages if sid == session_id)


@asynccontextmanager
async def fake_memory(memory):
    yield memory


def install_memory(monkeypatch, number, memory):
    implementation = load_agent_module(number)
    monkeypatch.setattr(implementation, "open_memory", lambda settings, **kw: fake_memory(memory))
    monkeypatch.setattr(
        implementation,
        "OpenAIEmbedder",
        lambda *a, **kw: SimpleNamespace(embed=AsyncMock(return_value=[0.1] * 3)),
    )
    return implementation


def responder(tool=None, arguments=None):
    seen = []

    def answer(messages, info):
        seen.append(info)
        if tool and len(seen) == 1:
            return ModelResponse(parts=[ToolCallPart(tool, arguments or {})])
        return ModelResponse(parts=[TextPart("Support response")])

    return FunctionModel(answer), seen


async def test_short_term_survives_a_new_agent_with_the_same_conversation(settings, monkeypatch):
    memory = Memory()
    install_memory(monkeypatch, 2, memory)
    async with open_agent(2, settings) as first:
        model, _ = responder()
        with first.agent.override(model=model):
            await first.chat("Remember Maya and the duplicate charge", "same-session")
    sent = []

    def answer(messages, info):
        sent.extend(messages)
        return ModelResponse(parts=[TextPart("Support response")])

    async with open_agent(2, settings) as second:
        with second.agent.override(model=FunctionModel(answer)):
            await second.chat("What did we discuss?", "same-session")
    # The earlier turns reach the model as PydanticAI message history, not prompt text.
    prior = [part.content for message in sent[:-1] for part in message.parts]
    assert prior == ["Remember Maya and the duplicate charge", "Support response"]


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_hydration_uses_sqlite_facts_and_updates_existing_entity(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.side_effect = None
    memory.query.cypher.return_value = [
        {"name": "Maya Chen", "type": "PERSON", "subtype": "CUSTOMER"},
        {"name": "Pro", "type": "OBJECT", "subtype": "PLAN"},
        {"name": "Invented Person", "type": "PERSON"},
    ]
    writer = SimpleNamespace(set_properties=AsyncMock())
    writes = writer.set_properties
    names = await hydration.hydrate_session_entities(
        memory, "session", settings.db_path, writer=writer
    )
    assert names == ["Maya Chen", "Pro"]
    properties = writes.await_args_list[0].args[2]
    assert properties["email"] == "maya.chen@northwind.example"
    assert properties["signup_date"] == "2025-03-14"
    assert properties["hydrated_from"] == "sqlite:customers"
    assert writes.await_args_list[1].args[2]["refund_limit"] == 250
    assert all(
        call.kwargs["resolve"] is False for call in memory.long_term.add_entity.await_args_list
    )
    # A system-of-record update must replace grounded facts on the same entity.
    from lib.db import connect

    with connect(settings.db_path) as conn:
        conn.execute(
            "UPDATE customers SET plan_id=(SELECT id FROM plans WHERE name='Enterprise') "
            "WHERE name='Maya Chen'"
        )
        conn.commit()
    await hydration.hydrate_session_entities(memory, "session", settings.db_path, writer=writer)
    assert writes.await_args_list[2].args[2]["plan"] == "Enterprise"


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_hydration_uses_resolved_aliases_without_renaming_nodes(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.side_effect = None
    memory.query.cypher.return_value = [
        {"name": "Maya", "type": "PERSON", "subtype": "CUSTOMER", "aliases": ["Maya Chen"]},
    ]
    writer = SimpleNamespace(set_properties=AsyncMock())
    writes = writer.set_properties
    assert await hydration.hydrate_session_entities(
        memory, "session", settings.db_path, writer=writer
    ) == ["Maya"]
    assert writes.call_args.args[0:2] == ("Maya", "PERSON")
    assert writes.call_args.args[2]["email"] == "maya.chen@northwind.example"
    assert memory.long_term.add_entity.call_args.args[0] == "Maya"
    # Conflicting exact aliases must not silently choose a customer's facts.
    memory.query.cypher.return_value[0]["aliases"].append("Ravi Shah")
    writes.reset_mock()
    assert (
        await hydration.hydrate_session_entities(memory, "session", settings.db_path, writer=writer)
        == []
    )
    writes.assert_not_called()


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_external_organizations_do_not_trigger_background_enrichment(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.side_effect = None
    memory.query.cypher.return_value = [
        {"name": "Stripe", "type": "ORGANIZATION", "subtype": "COMPANY"},
    ]
    writer = SimpleNamespace(set_properties=AsyncMock())
    writes = writer.set_properties
    hydrated = await hydration.hydrate_session_entities(
        memory, "session", settings.db_path, writer=writer
    )
    assert hydrated == []  # External data is not a SQLite-grounded fact.
    writes.assert_not_called()
    memory.long_term.add_entity.assert_not_awaited()


@pytest.mark.parametrize("number", [4, 5])
async def test_ablation_disables_both_paths_to_reasoning_but_still_records(
    number, settings, monkeypatch
):
    memory = Memory()
    install_memory(monkeypatch, number, memory)
    async with open_agent(number, settings, reasoning_retrieval=False) as chat:
        model, seen = responder("search_memory", {"query": "refund"})
        with chat.agent.override(model=model):
            reply = await chat.chat("Have you handled this?", "control")
    memory.reasoning.get_similar_traces.assert_not_called()
    memory.reasoning.start_trace.assert_awaited_once()
    assert "Past execution examples" not in seen[0].instructions
    assert not any(e["path"] == "reasoning_trace" for e in reply["context"]["evidence"])


@pytest.mark.parametrize("number", [4, 5])
async def test_reasoning_retrieval_failure_degrades_instead_of_failing(
    number, settings, monkeypatch
):
    memory = Memory()
    implementation = install_memory(monkeypatch, number, memory)
    monkeypatch.setattr(
        implementation, "similar_executions", AsyncMock(side_effect=RuntimeError("index"))
    )
    async with open_agent(number, settings) as chat:
        model, _ = responder()
        with chat.agent.override(model=model):
            reply = await chat.chat("Have you handled this?", "degraded")
    assert reply["execution_status"] == "succeeded"
    assert reply["status"] == "degraded"
    assert {"phase": "reasoning_retrieval", "error": "RuntimeError"} in reply["warnings"]
    memory.reasoning.complete_trace.assert_awaited_once()


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_preferences_are_read_through_the_library_user_lookup(number, settings):
    context = importlib.import_module(f"module_{number}.app.context")
    memory = Memory()
    memory.long_term.get_preferences_for.return_value = [
        SimpleNamespace(id="p1", preference="Email only", context=None, category="x:contact")
    ]
    rows = await context.search_preferences(memory, "maya@example.test", "workshop")
    memory.long_term.get_preferences_for.assert_awaited_once_with("workshop:maya@example.test")
    assert rows[0]["preference"] == "Email only"
    assert rows[0]["path"] == "customer_preference"
    assert await context.search_preferences(memory, None, "workshop") == []


@pytest.mark.parametrize("number", [2, 3, 4, 5])
async def test_local_memory_configuration_and_connection_lifetime(number, settings, monkeypatch):
    module = importlib.import_module(f"module_{number}.app.memory")
    captured = {}

    class Client:
        def __init__(self, configuration, **kwargs):
            captured.update(configuration=configuration, **kwargs)

        async def __aenter__(self):
            captured["opened"] = True
            return self

        async def __aexit__(self, *args):
            captured["closed"] = True

    monkeypatch.setattr(module, "MemoryClient", Client)
    async with module.open_memory(settings):
        assert captured["opened"]
        assert not captured.get("closed")
    assert captured["closed"]
    configuration = captured["configuration"]
    assert configuration.backend == "bolt"
    if number == 2:
        assert configuration.extraction.extractor_type == "none"
        assert "ontology" not in captured
    else:
        assert configuration.extraction.extractor_type == "llm"
        assert not configuration.enrichment.enabled
        assert captured["ontology"].domain.name == "acme-cloud-support"
        async with module.open_memory(settings, ontology="default-poleo"):
            assert captured["ontology"].domain.name == "generic-poleo"
        async with module.open_memory(settings, ontology="active"):
            assert captured["ontology"] is None
        with pytest.raises(ValueError):
            async with module.open_memory(settings, ontology="unknown"):
                pass


@pytest.mark.parametrize("number", range(1, 6))
def test_http_app_uses_the_local_factory(number, settings, monkeypatch):
    memory = Memory()
    if number > 1:
        install_memory(monkeypatch, number, memory)
    from lib import app_factory

    monkeypatch.setattr(app_factory, "get_settings", lambda: settings)
    application = importlib.reload(importlib.import_module(f"module_{number}.app.main")).app
    with TestClient(application) as client:
        chat = application.state.chat
        assert type(chat).__module__ == f"module_{number}.app.agent"
        assert client.get("/api/health").json()["module"] == number
        assert client.get("/api/health").json()["memory_layers"] == chat.memory_layers
        model, _ = responder()
        with chat.agent.override(model=model):
            response = client.post("/api/chat", json={"message": "Hello", "session_id": "web"})
            evaluation = client.get("/api/eval")
        assert response.status_code == 200
        assert response.json()["session_id"] == "workshop:web"
        assert evaluation.status_code == 200
        assert evaluation.json() == {"runs": []}
        if number == 1:
            assert client.get("/api/graph").json() == {"nodes": [], "relationships": []}
        if number < 5:
            assert client.get("/api/graph/nams").json()["unavailable"]


@pytest.mark.parametrize("bad", [0, 6, -1, "2", True])
def test_loader_rejects_invalid_stages(bad):
    with pytest.raises(ValueError):
        load_agent_module(bad)


def test_lesson_imports_do_not_hide_behavior_in_shared_or_previous_agents():
    forbidden = {"lib.chat", "lib.memory", "lib.hydrate", "lib.tools"}
    for number in range(1, 6):
        for path in (ROOT / f"module_{number}").rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    name = node.module or ""
                    assert name not in forbidden, path
                    assert not any(
                        name.startswith(f"module_{other}.")
                        for other in range(1, 6)
                        if other != number
                    ), path


@pytest.mark.parametrize("number", range(1, 6))
async def test_model_sees_refund_tool_only_with_full_scope(number, settings, monkeypatch):
    if number > 1:
        install_memory(monkeypatch, number, Memory())
    selected = {
        "account_email": "maya.chen@northwind.example",
        "incident_id": "maya-duplicate-compute",
        "authorize_refund": True,
    }
    async with open_agent(number, settings) as chat:
        for missing in [*selected, None]:
            scope = {key: value for key, value in selected.items() if key != missing}
            model, seen = responder()
            with chat.agent.override(model=model):
                await chat.chat("Show my refund history", "history", **scope)
            names = {tool.name for tool in seen[0].function_tools}
            assert "lookup_account" in names
            assert ("issue_refund" in names) == (missing is None)


@pytest.mark.parametrize("number", range(1, 6))
async def test_every_local_business_tool_returns_grounded_results(number, settings, monkeypatch):
    memory = Memory()
    if number > 1:
        install_memory(monkeypatch, number, memory)
    calls = [
        ("search_product_catalog", {"query": "compute"}),
        ("fetch_policy", {"topic": "refund"}),
        ("check_service_status", {"service": "Functions"}),
        (
            "issue_refund",
            {
                "customer_email": "maya.chen@northwind.example",
                "amount": 49,
                "reason": "duplicate charge",
            },
        ),
    ]
    index = 0

    def perform(messages, info):
        nonlocal index
        if index == len(calls):
            return ModelResponse(parts=[TextPart("Resolved")])
        tool, args = calls[index]
        index += 1
        return ModelResponse(parts=[ToolCallPart(tool, args)])

    async with open_agent(number, settings) as chat:
        with chat.agent.override(model=FunctionModel(perform)):
            result = await chat.chat(
                "Check products, policy, service and refund",
                "all-tools",
                account_email="maya.chen@northwind.example",
                incident_id="maya-duplicate-compute",
                authorize_refund=True,
            )
    observed = result["tool_calls"]
    assert [c["name"] for c in observed] == [name for name, _ in calls]
    assert observed[0]["output"]["count"] >= 1
    assert observed[1]["output"]["title"] == "Refund Policy"
    assert observed[2]["output"]["services"]
    assert observed[3]["output"]["status"] == "issued"
    assert all(c["duration_ms"] >= 0 and c["sql"] for c in observed)


@pytest.mark.parametrize("number", range(1, 6))
async def test_local_stage_and_retry_receipt(number, settings, monkeypatch):
    memory = Memory()
    if number > 1:
        install_memory(monkeypatch, number, memory)
    model, seen = responder("lookup_account", {"customer_email": "maya.chen@northwind.example"})
    async with open_agent(number, settings) as chat:
        with chat.agent.override(model=model):
            result = await chat.chat("Look up Maya", "lesson", request_id="retry")
            retry = await chat.chat("Look up Maya", "lesson", request_id="retry")
    assert retry == result
    assert result["session_id"] == "workshop:lesson"
    assert result["execution_status"] == "succeeded"
    assert result["tool_calls"][0]["output"]["plan"] == "Pro"
    assert result["tool_calls"][0]["sql"].startswith("SELECT")
    assert type(chat).__module__ == f"module_{number}.app.agent"
    assert len(seen) == 2
    if number >= 4:
        memory.reasoning.complete_trace.assert_awaited_once()


@pytest.mark.parametrize("number", [4, 5])
async def test_exception_and_rejection_complete_traces(number, settings, monkeypatch):
    memory = Memory()
    install_memory(monkeypatch, number, memory)
    async with open_agent(number, settings) as chat:

        def fail(*args):
            raise RuntimeError("model unavailable")

        with chat.agent.override(model=FunctionModel(fail)):
            result = await chat.chat(
                "refund 400",
                "decline",
                account_email="maya.chen@northwind.example",
                incident_id="maya-spot-capacity",
                authorize_refund=True,
            )
    assert result["execution_status"] == "failed"
    assert result["business_status"] == "rejected_over_limit"
    assert not any("INSERT INTO refunds" in (c["sql"] or "") for c in result["tool_calls"])
    outcome = memory.reasoning.complete_trace.call_args.kwargs["outcome"]
    assert not outcome.success
    assert outcome.error_kind == "execution_error"
    assert "rejected_over_limit" in outcome.summary


def test_replay_index_exposes_exact_conversations_for_live_graphs(settings, monkeypatch):
    import json

    from lib import app_factory

    monkeypatch.setattr(app_factory, "get_settings", lambda: settings)
    folder = settings.data_dir / "replays"
    folder.mkdir()
    (folder / "recorded.json").write_text(
        json.dumps(
            {
                "module": 4,
                "title": "Recorded case",
                "turns": [{"result": {"session_id": "namespace:first"}}],
                "branches": [{"turns": [{"result": {"session_id": "namespace:second"}}]}],
            }
        )
    )
    app = app_factory.create_app(load_agent_module(1).open_agent, title="Replay index")
    with TestClient(app) as client:
        run = client.get("/api/replays").json()["runs"][0]
    assert run["session_ids"] == ["namespace:first", "namespace:second"]
    assert run["module"] == 4 and run["title"] == "Recorded case"


@pytest.mark.parametrize("amount", [float("nan"), float("inf"), -float("inf")])
def test_http_nonfinite_refund_rejection_remains_json_safe(amount, settings, monkeypatch):
    from lib import app_factory

    monkeypatch.setattr(app_factory, "get_settings", lambda: settings)
    app = app_factory.create_app(load_agent_module(1).open_agent, title="Invalid refund")
    model, _ = responder(
        "issue_refund",
        {
            "customer_email": "maya.chen@northwind.example",
            "amount": amount,
            "reason": "invalid amount",
        },
    )
    with TestClient(app) as client, app.state.chat.agent.override(model=model):
        response = client.post(
            "/api/chat",
            json={
                "message": "Refund the charge",
                "account_email": "maya.chen@northwind.example",
                "incident_id": "maya-duplicate-compute",
                "authorize_refund": True,
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["business_status"] == "rejected_invalid_amount"
    assert isinstance(data["tool_calls"][0]["input"]["amount"], str)
    from lib.db import connect

    with connect(settings.db_path) as db:
        assert db.execute("SELECT count(*) FROM refunds").fetchone()[0] == 0


@pytest.mark.parametrize("number", [4, 5])
async def test_reasoning_retrieval_ignores_open_traces_including_this_turn(number):
    reasoning = importlib.import_module(f"module_{number}.app.reasoning")
    memory = Memory()
    embedder = SimpleNamespace(embed=AsyncMock(return_value=[0.1] * 3))
    await reasoning.similar_executions(memory, "Refund $49", embedder, "workshop")
    query, _ = memory.query.cypher.call_args.args
    # This turn's trace is opened before retrieval; it must never match itself.
    assert "t.completed_at IS NOT NULL" in query
