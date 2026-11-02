#!/usr/bin/env python3
"""make reset-memory — wipe the Neo4j memory graph (destructive, confirms first)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    from neo4j import GraphDatabase

    from lib.settings import get_settings

    s = get_settings()
    if not s.neo4j_uri:
        print("NEO4J_URI not set — see .env.example")
        return 1
    answer = input(
        f"This deletes ALL nodes and relationships in {s.neo4j_uri} "
        f"(database '{s.neo4j_database}'). Type 'wipe' to continue: "
    )
    if answer.strip() != "wipe":
        print("Aborted.")
        return 1
    with GraphDatabase.driver(s.neo4j_uri, auth=(s.neo4j_username, s.neo4j_password)) as driver:
        driver.execute_query("MATCH (n) DETACH DELETE n", database_=s.neo4j_database)
    print("Memory graph wiped. Re-run make module-N to rebuild state.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
