from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from scripts import seed_sqlite


@pytest.mark.parametrize("number", [3, 4, 5])
async def test_product_facts_never_hydrate_an_organization(number, tmp_path, monkeypatch):
    from importlib import import_module

    module = import_module(f"module_{number}.app.hydrate")
    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    memory = SimpleNamespace(
        query=SimpleNamespace(
            cypher=AsyncMock(
                return_value=[
                    {"name": "Acme Cloud Compute", "type": "ORGANIZATION", "aliases": []},
                ]
            )
        ),
        long_term=SimpleNamespace(add_entity=AsyncMock()),
    )
    assert await module.hydrate_session_entities(memory, "session", seed_sqlite.DB_PATH) == []
    memory.long_term.add_entity.assert_not_called()
