"""Property hydration (module 3): extracted entities get their FACTS from the
SQLite system of record — never from the LLM.

Two write paths, verified in spike 0.5 (docs/verification-log.md):
  1. `add_entity` public upsert — MERGEs on (name, type), ON MATCH updates the
     `description` (but NOT metadata/attributes — an upstream limitation).
  2. Flat node properties via our own driver session (`SET e += $map`) —
     hydrated facts (email, plan, plan_tier, …) become first-class node
     properties, visible directly in the NVL details panel.
"""

from __future__ import annotations

from typing import Any

from neo4j import AsyncGraphDatabase
from neo4j_agent_memory import MemoryClient

from . import db as dbx

MENTIONED_ENTITIES_CYPHER = """
MATCH (c:Conversation {session_id: $session_id})-[:HAS_MESSAGE]->(m:Message)
MATCH (m)-[:MENTIONS]->(e:Entity)
RETURN DISTINCT e.name AS name, e.type AS type, e.subtype AS subtype
"""

SET_FLAT_ATTRIBUTES_CYPHER = """
MATCH (e:Entity {name: $name, type: $type})
SET e += $attributes
"""


def _lookup_hydration(db_path, name: str) -> dict[str, Any] | None:
    """Map an extracted entity onto grounded facts from the system of record."""
    lname = name.lower()
    with dbx.connect(db_path) as conn:
        row = conn.execute(
            "SELECT c.name, c.email, c.signup_date, c.preferred_contact, "
            "o.name AS organization, p.name AS plan, p.tier AS plan_tier "
            "FROM customers c LEFT JOIN organizations o ON c.organization_id = o.id "
            "LEFT JOIN plans p ON c.plan_id = p.id WHERE lower(c.name) = ?",
            (lname,),
        ).fetchone()
        if row:
            r = dict(row)
            return {
                "description": (
                    f"{r['name']} — {r['plan']} plan customer at "
                    f"{r['organization']}, signed up {r['signup_date']}."
                ),
                "attributes": {
                    "email": r["email"],
                    "plan": r["plan"],
                    "plan_tier": r["plan_tier"],
                    "signup_date": r["signup_date"],
                    "preferred_contact": r["preferred_contact"],
                    "organization": r["organization"],
                    "hydrated_from": "sqlite:customers",
                },
            }
        row = conn.execute(
            "SELECT name, sku, description, category FROM products WHERE lower(name) = ?",
            (lname,),
        ).fetchone()
        if row:
            r = dict(row)
            return {
                "description": r["description"],
                "attributes": {
                    "sku": r["sku"],
                    "category": r["category"],
                    "hydrated_from": "sqlite:products",
                },
            }
        row = conn.execute(
            "SELECT name, tier, monthly_price, refund_limit FROM plans WHERE lower(name) = ?",
            (lname,),
        ).fetchone()
        if row:
            r = dict(row)
            return {
                "description": (
                    f"{r['name']} plan — ${r['monthly_price']:.2f}/mo, "
                    f"no-approval refund limit ${r['refund_limit']:.2f}."
                ),
                "attributes": {
                    "tier": r["tier"],
                    "monthly_price": r["monthly_price"],
                    "refund_limit": r["refund_limit"],
                    "hydrated_from": "sqlite:plans",
                },
            }
        row = conn.execute(
            "SELECT name, industry FROM organizations WHERE lower(name) = ?", (lname,)
        ).fetchone()
        if row:
            r = dict(row)
            return {
                "description": f"{r['name']} ({r['industry']}) — Acme Cloud customer organization.",
                "attributes": {"industry": r["industry"], "hydrated_from": "sqlite:organizations"},
            }
    return None


async def _apply_flat_attributes(s, name: str, etype: str, attributes: dict) -> None:
    """Write hydrated facts as first-class node properties via our own driver
    (the memory client's public Cypher surface is read-only)."""
    driver = AsyncGraphDatabase.driver(
        s.neo4j_uri, auth=(s.neo4j_username, s.neo4j_password)
    )
    try:
        async with driver.session(database=s.neo4j_database) as session:
            await session.run(
                SET_FLAT_ATTRIBUTES_CYPHER,
                {"name": name, "type": etype, "attributes": attributes},
            )
    finally:
        await driver.close()


async def hydrate_session_entities(
    client: MemoryClient, session_id: str, db_path, settings=None
) -> list[str]:
    """Upsert grounded properties onto every entity mentioned in this session.

    Returns the names of hydrated entities (for logging/tests). `settings` is
    required for the flat-attribute write path (driver credentials).
    """
    rows = await client.query.cypher(MENTIONED_ENTITIES_CYPHER, {"session_id": session_id})
    hydrated: list[str] = []
    for row in rows:
        facts = _lookup_hydration(db_path, row["name"])
        if facts is None:
            continue
        # 1. Public upsert: refreshes the grounded description.
        await client.long_term.add_entity(
            row["name"],
            row["type"],
            subtype=row.get("subtype"),
            description=facts["description"],
            resolve=False,  # the node already exists; hydrate it directly
        )
        # 2. Flat properties (upstream add_entity does not write attributes on
        #    the ON MATCH path — see docs/verification-log.md, spike 0.5).
        if settings is not None:
            await _apply_flat_attributes(settings, row["name"], row["type"], facts["attributes"])
        hydrated.append(row["name"])
    return hydrated
