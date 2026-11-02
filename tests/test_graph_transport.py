from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from lib.graph import bolt_graph


@pytest.mark.asyncio
async def test_populated_graph_uses_serialized_maps_and_preserves_identity():
    query = AsyncMock(
        return_value=[
            {
                "n": {
                    "id": "node-1",
                    "labels": ["Preference"],
                    "properties": {
                        "preference": "email",
                        "embedding": [0.1],
                        "task_embedding": [0.2],
                        "created_at": datetime(2026, 11, 1, tzinfo=UTC),
                    },
                },
                "m": {"id": "node-2", "labels": ["Entity"], "properties": {"name": "Maya"}},
                "r": {
                    "id": "edge-1",
                    "from": "node-1",
                    "to": "node-2",
                    "type": "APPLIES_TO",
                    "properties": {},
                },
            }
        ]
    )
    graph = await bolt_graph(
        SimpleNamespace(query=SimpleNamespace(cypher=query)),
        "long_term",
        session_id="lesson-session",
    )
    assert graph["relationships"][0]["from"] == "node-1"
    assert graph["nodes"][0]["properties"] == {
        "preference": "email",
        "created_at": "2026-11-01T00:00:00+00:00",
    }
    assert "Preference" in query.call_args.args[1]["labels"]
    assert query.call_args.args[1]["session_id"] == "lesson-session"
    assert graph["truncated"] is False
