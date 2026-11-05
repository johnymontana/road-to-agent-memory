#!/usr/bin/env python3
"""Repeatable instructor recipes: local validation and a private SQL plan upgrade/rollback."""

from __future__ import annotations

import argparse
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def strict_demo():
    from neo4j_agent_memory import load_ontology
    from neo4j_agent_memory.extraction.base import (
        ExtractedEntity,
        ExtractedRelation,
        ExtractionResult,
    )

    ontology = load_ontology("module_3/ontology/acme_cloud.yaml")
    fixture = ExtractionResult(
        entities=[
            ExtractedEntity(name="Maya Chen", type="PERSON", subtype="CUSTOMER"),
            ExtractedEntity(name="Pro", type="OBJECT", subtype="PLAN"),
        ],
        relations=[
            ExtractedRelation(source="Maya Chen", target="Pro", relation_type="INVENTED_RELATION")
        ],
    )
    clean, dropped = fixture.validate_relations(ontology, mode="drop")
    assert not clean.relations and len(dropped) == 1
    print("Permissive: invalid relationship dropped.")
    try:
        fixture.validate_relations(ontology, mode="raise")
    except Exception as error:
        print("Strict: invalid relationship raises", type(error).__name__)
    else:
        raise AssertionError("Strict validation did not raise")


async def plan_demo():
    """Real hydrator + private SQL + deterministic local graph-writer fixture."""
    from types import SimpleNamespace

    from lib.db import connect, lookup_account
    from lib.settings import get_settings
    from module_3.app.hydrate import hydrate_session_entities

    settings = get_settings()
    nodes = {}
    writes = []

    class LocalFixture:
        async def cypher(self, query, parameters):
            return [{"name": "Maya Chen", "type": "PERSON", "subtype": "CUSTOMER", "aliases": []}]

        async def add_entity(self, name, etype, **kwargs):
            node = nodes.setdefault((name, etype), {"id": "local-maya"})
            node["description"] = kwargs["description"]

        async def set_properties(self, name, etype, attributes):
            nodes[(name, etype)].update(attributes)
            writes.append(dict(attributes))

    adapter = LocalFixture()
    memory = SimpleNamespace(query=adapter, long_term=adapter)
    with tempfile.TemporaryDirectory(prefix="workshop-plan-") as temp:
        path = Path(temp) / "acme_cloud.db"
        with sqlite3.connect(settings.db_path) as source, sqlite3.connect(path) as target:
            source.backup(target)
        with connect(path) as db:
            before = lookup_account(db, "maya.chen@northwind.example")["plan"]

        async def snapshot(expected):
            names = await hydrate_session_entities(
                memory, "local-fixture", path, message_id="local-message", writer=adapter
            )
            assert names == ["Maya Chen"] and len(nodes) == 1
            node = nodes[("Maya Chen", "PERSON")]
            assert node["plan"] == expected and node["email"] == "maya.chen@northwind.example"
            assert node["hydrated_from"] == "sqlite:customers"
            print("Local hydrated entity:", node["id"], node["plan"], node["hydrated_from"])

        await snapshot(before)
        try:
            with connect(path) as db:
                db.execute(
                    "UPDATE customers SET plan_id=(SELECT id FROM plans WHERE "
                    "name='Enterprise') WHERE email='maya.chen@northwind.example'"
                )
            await snapshot("Enterprise")
        finally:
            with connect(path) as db:
                db.execute(
                    (
                        "UPDATE customers SET plan_id=(SELECT id FROM plans WHERE name=?) "
                        "WHERE email='maya.chen@northwind.example'"
                    ),
                    (before,),
                )
            await snapshot(before)
        assert len(writes) == 3
        print(
            "Actual hydration verified before/after/restoration on one local "
            "fixture entity. Participant SQL and Neo4j unchanged."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe", choices=["strict", "plan"])
    args = parser.parse_args()
    if args.recipe == "strict":
        strict_demo()
    else:
        import asyncio

        asyncio.run(plan_demo())
