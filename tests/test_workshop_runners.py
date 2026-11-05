"""Check that scenario playback, eval, and fresh-skill runs select lesson code."""

from __future__ import annotations

import importlib
import json
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from pydantic_ai.messages import ModelResponse, TextPart
from pydantic_ai.models.function import FunctionModel

from lib.settings import AppSettings


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch, tmp_path):
    from lib import settings

    def configured():
        return AppSettings(_env_file=None, openai_api_key="test-key", data_dir=tmp_path)

    configured.cache_clear = lambda: None
    monkeypatch.setattr(settings, "get_settings", configured)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")


@pytest.mark.parametrize("number", range(1, 6))
async def test_scenario_runner_uses_selected_lesson(number, monkeypatch):
    from scripts import run_scenario

    lesson = importlib.import_module(f"module_{number}.app.agent")
    calls = []
    chat = SimpleNamespace(
        chat=AsyncMock(
            return_value={
                "reply": "Done",
                "tool_calls": [],
                "context": {"summary": None},
                "timing": {},
                "warnings": [],
            }
        )
    )

    @asynccontextmanager
    async def factory(settings, **options):
        calls.append(options)
        yield chat

    monkeypatch.setattr(lesson, "open_agent", factory)
    monkeypatch.setattr(run_scenario, "TURN_PAUSE_S", 0)
    await run_scenario.run_sessions(
        {"name": "scenario"}, number, [{"id": "a", "messages": ["hello"]}]
    )
    assert calls == [{}]
    assert chat.chat.call_args.args == ("hello",)
    assert chat.chat.call_args.kwargs["session_id"] == "a"
    assert chat.chat.call_args.kwargs["request_id"]


@pytest.mark.parametrize("mode", ["on", "off", "fallback"])
async def test_fresh_agent_loads_skill_only_and_calls_no_memory(mode, monkeypatch, tmp_path):
    from module_5.app import fresh_agent

    for directory in ["distilled", "pre-distilled-skill"]:
        path = tmp_path / "artifacts" / directory
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"Unique {directory} procedure")
    monkeypatch.setattr(fresh_agent, "ROOT", tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    settings = AppSettings(_env_file=None, openai_api_key="test-key", data_dir=tmp_path)
    real_factory = fresh_agent.create_fresh_agent
    seen = []
    managers = []

    def response(messages, info):
        seen.append(info)
        return ModelResponse(parts=[TextPart("Handled cold")])

    def factory(settings, **kwargs):
        agent = real_factory(settings, **kwargs)
        override = agent.override(model=FunctionModel(response))
        override.__enter__()
        managers.append(override)
        return agent

    monkeypatch.setattr(fresh_agent, "create_fresh_agent", factory)
    try:
        result = await fresh_agent.run_fresh_agent(settings, mode=mode)
    finally:
        for manager in reversed(managers):
            manager.__exit__(None, None, None)
    assert result["with_skill"] is (mode != "off")
    assert result["reply"] == "Handled cold"
    names = {tool.name for tool in seen[0].function_tools}
    assert "search_memory" not in names
    if mode == "off":
        assert "Unique" not in seen[0].instructions
    else:
        directory = "distilled" if mode == "on" else "pre-distilled-skill"
        assert f"Unique {directory} procedure" in seen[0].instructions


def test_missing_or_invalid_skill_is_never_silently_a_control(monkeypatch, tmp_path):
    from module_5.app import fresh_agent

    monkeypatch.setattr(fresh_agent, "ROOT", tmp_path)
    with pytest.raises(FileNotFoundError):
        fresh_agent.load_skill("on")
    with pytest.raises(ValueError):
        fresh_agent.load_skill("bogus")


async def test_eval_preserves_partial_results_and_rejects_denials():
    from scripts.eval import run_eval

    chat = SimpleNamespace(
        chat=AsyncMock(
            side_effect=[
                {"reply": "I do not know"},
                RuntimeError("routing"),
                {"reply": '{"fact":"correct","source_ids":["source"]}'},
            ]
        )
    )
    questions = [
        {
            "id": str(i),
            "question": "fact?",
            "session": str(i),
            "expected": {"fact": "correct"},
            "source_ids": ["source"],
        }
        for i in range(3)
    ]
    partial = []
    result = await run_eval(chat, questions, on_result=lambda rows: partial.append(list(rows)))
    assert [q["answered"] for q in result["questions"]] == [False, False, True]
    assert result["questions"][1]["error"] == "RuntimeError"
    assert [len(rows) for rows in partial] == [1, 2, 3]


async def test_eval_private_sql_and_tool_allowances(monkeypatch, tmp_path):
    import hashlib
    import sqlite3

    from lib import workshop
    from scripts import eval as evaluation
    from scripts import seed_sqlite

    settings = AppSettings(_env_file=None, data_dir=tmp_path, openai_api_key="test-key")
    monkeypatch.setattr(seed_sqlite, "DB_PATH", settings.db_path)
    seed_sqlite.main()
    before = hashlib.sha256(settings.db_path.read_bytes()).hexdigest()
    options = []

    @asynccontextmanager
    async def factory(module, private, **kwargs):
        options.append(kwargs)
        assert private.data_dir != settings.data_dir
        with sqlite3.connect(private.db_path) as db:
            assert (
                db.execute("SELECT name FROM customers WHERE id=1")
                .fetchone()[0]
                .startswith("Maya Eval")
            )
        yield SimpleNamespace(module=module, chat=AsyncMock(return_value={"reply": "{}"}))

    monkeypatch.setattr(workshop, "open_agent", factory)
    monkeypatch.setattr(
        evaluation,
        "seed_fixture",
        AsyncMock(return_value={"message": [], "entity": [], "trace": []}),
    )
    result = await evaluation.run_isolated_eval(4, settings)
    assert result["status"] == "completed" and len(result["questions"]) == 4
    assert options == [
        {
            "business_tools": False,
            "evaluation": True,
            "record_reasoning": False,
            "reasoning_namespace": "eval-" + result["id"],
        }
    ]
    assert hashlib.sha256(settings.db_path.read_bytes()).hexdigest() == before


async def test_restart_appends_each_turn_once_and_retains_both_processes(monkeypatch, tmp_path):
    from lib import workshop
    from scripts import run_scenario

    settings = AppSettings(_env_file=None, data_dir=tmp_path)
    prior = {
        "id": "restart",
        "pid": 123,
        "turns": [
            {
                "message": "head",
                "namespace": "ns",
                "result": {"reply": "head reply", "tool_calls": []},
            }
        ],
    }
    run_scenario.save_replay(settings, prior)
    chat = SimpleNamespace(
        chat=AsyncMock(
            return_value={"reply": "tail reply", "tool_calls": [], "timing": {}, "warnings": []}
        )
    )

    @asynccontextmanager
    async def factory(*args, **kwargs):
        yield chat

    monkeypatch.setattr(workshop, "open_agent", factory)
    monkeypatch.setattr(run_scenario, "TURN_PAUSE_S", 0)
    await run_scenario.run_sessions(
        {"name": "restart"},
        2,
        [{"id": "a", "messages": ["tail one", "tail two"]}],
        settings=settings,
        run_id="restart",
        append=True,
    )
    report = json.loads((tmp_path / "replays/restart.json").read_text())
    assert [t["message"] for t in report["turns"]] == ["head", "tail one", "tail two"]
    assert report["process_ids"][0] == 123 and len(report["process_ids"]) == 2
    assert report["status"] == "completed" and len(report["graph"]["nodes"]) == 3
