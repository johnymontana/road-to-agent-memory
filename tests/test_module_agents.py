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
            add_entity=AsyncMock(),
        )
        self.query = SimpleNamespace(cypher=AsyncMock(return_value=[]))
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
            complete_trace=AsyncMock(return_value=self.trace),
        )

    async def create(self, session_id):
        self.events.append(("conversation", session_id))

    async def add(self, session_id, role, content):
        self.events.append(("write", role))
        self.messages.append((session_id, role, content))

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
    return implementation


def responder(tool=None, arguments=None):
    seen = []

    def answer(messages, info):
        seen.append(info)
        if tool and len(seen) == 1:
            return ModelResponse(parts=[ToolCallPart(tool, arguments or {})])
        return ModelResponse(parts=[TextPart("Support response")])

    return FunctionModel(answer), seen


@pytest.mark.parametrize("number", range(1, 6))
async def test_agent_stage_runs_local_business_tool_and_preserves_contract(
    number, settings, monkeypatch
):
    memory = Memory()
    implementation = load_agent_module(number)
    if number > 1:
        install_memory(monkeypatch, number, memory)
    model, seen = responder("lookup_account", {"customer_email": "maya.chen@northwind.example"})
    async with open_agent(number, settings) as chat:
        assert type(chat).__module__ == f"module_{number}.app.agent"
        with chat.agent.override(model=model):
            reply = await chat.chat("Look up my account", "test-session")
        assert chat.module == number
        assert chat.memory_layers == ["short_term", "long_term", "reasoning"][: min(number - 1, 3)]
        names = {tool.name for tool in seen[0].function_tools}
        assert names == BUSINESS_TOOLS | (MEMORY_TOOLS if number >= 3 else set())
        if number >= 3:
            assert "MUST call `save_preference`" in seen[0].instructions
        assert reply["session_id"] == "test-session"
        assert reply["reply"] == "Support response"
        call = reply["tool_calls"][0]
        assert call["name"] == "lookup_account"
        assert call["output"]["plan"] == "Pro"
        assert "SELECT" in call["sql"]
        if number == 1:
            assert chat.memory is None
            assert reply["context"] == {"used_memory": False, "summary": None}
        else:
            assert memory.events == [
                ("conversation", "test-session"),
                ("write", "user"),
                ("retrieve", "test-session"),
                ("write", "assistant"),
            ]
            assert "Retrieved memory" in seen[0].instructions
            assert memory.context_options == [
                {
                    "include_long_term": number >= 3,
                    "include_reasoning": False,
                }
            ]
        if number < 4:
            memory.reasoning.start_trace.assert_not_called()
            memory.reasoning.get_similar_traces.assert_not_called()
        else:
            # Exercise the library's real record_agent_trace against the fake backend.
            memory.reasoning.record_tool_call.assert_awaited_once()
            assert (
                memory.reasoning.record_tool_call.call_args.kwargs["tool_name"] == "lookup_account"
            )
            assert memory.reasoning.complete_trace.call_args.kwargs["success"] is True
            assert "Similar tasks" in seen[0].instructions
            # Failed executions are part of this lesson's recall, too.
            assert memory.reasoning.get_similar_traces.call_args.kwargs["success_only"] is False
    # Agent construction itself must come from this lesson, not shared dispatch.
    assert implementation.ChatService.__module__ == f"module_{number}.app.agent"


async def test_short_term_survives_a_new_agent_with_the_same_conversation(settings, monkeypatch):
    memory = Memory()
    install_memory(monkeypatch, 2, memory)
    async with open_agent(2, settings) as first:
        model, _ = responder()
        with first.agent.override(model=model):
            await first.chat("Remember Maya and the duplicate charge", "same-session")
    async with open_agent(2, settings) as second:
        model, seen = responder()
        with second.agent.override(model=model):
            await second.chat("What did we discuss?", "same-session")
        assert "Remember Maya and the duplicate charge" in seen[0].instructions


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_hydration_uses_sqlite_facts_and_updates_existing_entity(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.return_value = [
        {"name": "Maya Chen", "type": "PERSON", "subtype": "CUSTOMER"},
        {"name": "Pro", "type": "OBJECT", "subtype": "PLAN"},
        {"name": "Invented Person", "type": "PERSON"},
    ]
    writes = AsyncMock()
    monkeypatch.setattr(hydration, "_apply_flat_attributes", writes)
    names = await hydration.hydrate_session_entities(memory, "session", settings.db_path, settings)
    assert names == ["Maya Chen", "Pro"]
    properties = writes.await_args_list[0].args[3]
    assert properties["email"] == "maya.chen@northwind.example"
    assert properties["signup_date"] == "2025-03-14"
    assert properties["hydrated_from"] == "sqlite:customers"
    assert writes.await_args_list[1].args[3]["refund_limit"] == 250
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
    await hydration.hydrate_session_entities(memory, "session", settings.db_path, settings)
    assert writes.await_args_list[2].args[3]["plan"] == "Enterprise"


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_hydration_uses_resolved_aliases_without_renaming_nodes(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.return_value = [
        {"name": "Maya", "type": "PERSON", "subtype": "CUSTOMER", "aliases": ["Maya Chen"]},
    ]
    writes = AsyncMock()
    monkeypatch.setattr(hydration, "_apply_flat_attributes", writes)
    assert await hydration.hydrate_session_entities(
        memory, "session", settings.db_path, settings
    ) == ["Maya"]
    assert writes.call_args.args[1:3] == ("Maya", "PERSON")
    assert writes.call_args.args[3]["email"] == "maya.chen@northwind.example"
    assert memory.long_term.add_entity.call_args.args[0] == "Maya"
    # Conflicting exact aliases must not silently choose a customer's facts.
    memory.query.cypher.return_value[0]["aliases"].append("Ravi Shah")
    writes.reset_mock()
    assert (
        await hydration.hydrate_session_entities(memory, "session", settings.db_path, settings)
        == []
    )
    writes.assert_not_called()


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_extracted_third_party_organizations_are_queued_for_enrichment(
    number, settings, monkeypatch
):
    hydration = importlib.import_module(f"module_{number}.app.hydrate")
    memory = Memory()
    memory.query.cypher.return_value = [
        {"name": "Stripe", "type": "ORGANIZATION", "subtype": "COMPANY"},
    ]
    writes = AsyncMock()
    monkeypatch.setattr(hydration, "_apply_flat_attributes", writes)
    hydrated = await hydration.hydrate_session_entities(
        memory, "session", settings.db_path, settings
    )
    assert hydrated == []  # External data is not a SQLite-grounded fact.
    writes.assert_not_called()
    memory.long_term.add_entity.assert_awaited_once_with(
        "Stripe",
        "ORGANIZATION",
        subtype="COMPANY",
        resolve=False,
        deduplicate=False,
        enrich=True,
    )


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_memory_tools_search_grounded_entities_and_collect_preferences(
    number, settings, monkeypatch
):
    memory = Memory()
    install_memory(monkeypatch, number, memory)
    memory.long_term.search_entities.return_value = [
        SimpleNamespace(name="Maya Chen", description="Signed up 2025-03-14"),
    ]
    async with open_agent(number, settings) as chat:
        model, _ = responder("search_memory", {"query": "Maya"})
        with chat.agent.override(model=model):
            reply = await chat.chat("Find Maya", "search-session")
        call = reply["tool_calls"][0]
        assert call["sql"] is None
        assert "2025-03-14" in call["output"]
        model, _ = responder("save_preference", {"category": "contact", "preference": "email"})
        with chat.agent.override(model=model):
            reply = await chat.chat("Please use email", "preference-session")
        assert reply["tool_calls"][0]["name"] == "save_preference"
        memory.long_term.add_preference.assert_awaited_once_with("contact", "email", context=None)
        memory.long_term.search_preferences.return_value = [
            SimpleNamespace(category="contact", preference="email"),
        ]
        model, _ = responder("recall_preferences", {"topic": "contact"})
        with chat.agent.override(model=model):
            reply = await chat.chat("How do I prefer follow-ups?", "recall-session")
        assert "[contact] email" in reply["tool_calls"][0]["output"]
        if number == 3:
            memory.reasoning.get_similar_traces.assert_not_called()
        else:
            assert memory.reasoning.get_similar_traces.call_args.kwargs["success_only"] is False


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
    assert "Similar tasks" not in seen[0].instructions
    assert "reasoning" not in reply["context"]["summary"]


@pytest.mark.parametrize("number", [4, 5])
async def test_rejected_refund_is_a_failed_recorded_trace(number, settings, monkeypatch):
    memory = Memory()
    install_memory(monkeypatch, number, memory)
    model, _ = responder(
        "issue_refund",
        {
            "customer_email": "maya.chen@northwind.example",
            "amount": 400,
            "reason": "spot capacity",
        },
    )
    async with open_agent(number, settings) as chat:
        with chat.agent.override(model=model):
            reply = await chat.chat("Refund $400", "failed-refund")
    assert reply["tool_calls"][0]["output"]["status"] == "rejected_over_limit"
    completion = memory.reasoning.complete_trace.call_args.kwargs
    assert completion["success"] is False
    assert "Refund rejected" in completion["outcome"]


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
        assert configuration.enrichment.enabled
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
        assert response.json()["session_id"] == "web"
        assert evaluation.status_code == 200
        assert len(evaluation.json()["questions"]) == 4
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
            result = await chat.chat("Check products, policy, service and refund", "all-tools")
    observed = result["tool_calls"]
    assert [c["name"] for c in observed] == [name for name, _ in calls]
    assert observed[0]["output"]["count"] >= 1
    assert observed[1]["output"]["title"] == "Refund Policy"
    assert observed[2]["output"]["services"]
    assert observed[3]["output"]["status"] == "issued"
    assert all(c["duration_ms"] >= 0 and c["sql"] for c in observed)
