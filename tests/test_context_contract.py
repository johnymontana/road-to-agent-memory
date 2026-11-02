from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


@pytest.mark.parametrize("number", [2, 3, 4, 5])
async def test_recent_history_keeps_the_newest_ten_in_chronological_order(number):
    from importlib import import_module

    module = import_module(f"module_{number}.app.context")
    rows = [{"id": str(n), "role": "user", "content": f"turn {n}"} for n in range(12, 2, -1)]
    memory = SimpleNamespace(query=SimpleNamespace(cypher=AsyncMock(return_value=rows)))
    evidence = await module.recent_messages(memory, "session", exclude_id="current")
    assert [r["content"] for r in evidence] == [f"turn {n}" for n in range(3, 13)]
    query, params = memory.query.cypher.call_args.args
    assert "DESC" in query
    assert params["exclude_id"] == "current"
