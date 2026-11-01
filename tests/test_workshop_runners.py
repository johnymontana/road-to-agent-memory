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
def isolated_configuration(monkeypatch):
    from lib import settings

    def configured():
        return AppSettings(_env_file=None, openai_api_key="test-key")

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
    chat.chat.assert_awaited_once_with("hello", session_id="scenario-a")


async def test_ablation_passes_options_without_mutating_process_environment(monkeypatch, tmp_path):
    from scripts import run_scenario

    scenario = {"name": "repeat", "description": "ablation", "sessions": []}
    (tmp_path / "repeat.json").write_text(json.dumps(scenario))
    monkeypatch.setattr(run_scenario, "SCENARIOS", tmp_path)
    monkeypatch.setattr("sys.argv", ["run_scenario.py", "repeat", "--module", "4", "--ablation"])
    monkeypatch.setenv("AGENT_REASONING_RETRIEVAL", "original")
    runner = AsyncMock()
    monkeypatch.setattr(run_scenario, "run_sessions", runner)
    await run_scenario.main()
    assert [c.kwargs for c in runner.await_args_list] == [
        {"reasoning_retrieval": False},
        {"reasoning_retrieval": True},
    ]
    import os

    assert os.environ["AGENT_REASONING_RETRIEVAL"] == "original"


async def test_eval_uses_selected_lesson_and_four_questions(monkeypatch, capsys):
    from scripts import eval as evaluation

    lesson = importlib.import_module("module_3.app.agent")
    chat = SimpleNamespace(
        module=3, chat=AsyncMock(return_value={"reply": "Maya charged in March 2025"})
    )

    @asynccontextmanager
    async def factory(settings):
        yield chat

    monkeypatch.setattr(lesson, "open_agent", factory)
    monkeypatch.setattr("sys.argv", ["eval.py", "--module", "3"])
    await evaluation.main()
    assert chat.chat.await_count == 5  # Priming exchange plus four eval questions.
    assert "module 3" in capsys.readouterr().out


@pytest.mark.parametrize("mode", ["on", "off", "fallback"])
async def test_fresh_agent_loads_skill_only_and_calls_no_memory(mode, monkeypatch, tmp_path):
    from module_5.app import fresh_agent

    for directory in ["distilled", "pre-distilled-skill"]:
        path = tmp_path / "artifacts" / directory
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"Unique {directory} procedure")
    monkeypatch.setattr(fresh_agent, "ROOT", tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    settings = AppSettings(_env_file=None, openai_api_key="test-key")
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
