#!/usr/bin/env python3
"""make check — the pre-work and module-0 smoke test. Prints a green/red checklist."""

from __future__ import annotations

import asyncio
import os
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OK, FAIL, WARN = "✅", "❌", "⚠️ "


def main() -> int:
    from lib.settings import get_settings

    s = get_settings()
    failures = 0

    def report(ok: bool, label: str, detail: str = "") -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"  {OK if ok else FAIL} {label}" + (f" — {detail}" if detail else ""))

    print("Road to Agent Memory — environment check\n")

    report(bool(s.neo4j_uri), "NEO4J_URI set")
    report(bool(s.neo4j_password), "NEO4J_PASSWORD set")
    report(bool(s.openai_api_key), "OPENAI_API_KEY set (env or personal Codespaces secret)")
    try:
        with sqlite3.connect(f"file:{s.db_path}?mode=ro", uri=True) as db:
            for table in ("customers", "plans", "policies", "products", "service_status"):
                assert db.execute(f"SELECT count(*) FROM {table}").fetchone()[0] > 0, table
        report(True, "SQLite schema and lesson data")
    except Exception as error:
        report(False, "SQLite schema and lesson data", type(error).__name__)

    bolt_ready = False
    model_ready = False
    if s.neo4j_uri and s.neo4j_password:
        try:
            from neo4j import GraphDatabase

            with GraphDatabase.driver(
                s.neo4j_uri, auth=(s.neo4j_username, s.neo4j_password)
            ) as driver:
                driver.verify_connectivity()
                # Median of a few trivial queries ≈ the cost of every memory read/write.
                timings = []
                for _ in range(5):
                    started = time.monotonic()
                    driver.execute_query("RETURN 1", database_=s.neo4j_database)
                    timings.append(time.monotonic() - started)
                query_ms = round(sorted(timings)[2] * 1000)
            bolt_ready = True
            report(True, "AuraDB reachable (Bolt)", f"{query_ms} ms per query")
        except Exception as exc:  # noqa: BLE001 — report anything to the attendee
            report(
                False,
                "AuraDB reachable (Bolt)",
                f"{type(exc).__name__} — check network, database and credentials",
            )

    if s.openai_api_key:
        try:
            from openai import OpenAI

            with OpenAI(api_key=s.openai_api_key, timeout=20, max_retries=1) as client:
                client.chat.completions.create(
                    model=s.openai_model,
                    messages=[{"role": "user", "content": "Reply OK"}],
                    max_completion_tokens=8,
                )
                result = client.embeddings.create(
                    model=s.embedding_model, input="workshop capability check"
                )
                assert result.data[0].embedding
            model_ready = True
            report(True, "Configured chat model and embeddings")
        except Exception as error:
            report(False, "Configured chat model and embeddings", type(error).__name__)
    if bolt_ready and model_ready:

        async def memory_capability():
            from lib.graph import bolt_graph
            from module_2.app.memory import open_memory

            async with open_memory(s) as memory:
                graph = await bolt_graph(memory, limit=3)
                assert all(
                    edge["from"] in {n["id"] for n in graph["nodes"]}
                    for edge in graph["relationships"]
                )

        try:
            print(
                "  Checking memory startup and graph serialization (may take a minute)…", flush=True
            )
            asyncio.run(asyncio.wait_for(memory_capability(), timeout=180))
            report(True, "Memory startup and graph transport")
        except Exception as error:
            report(False, "Memory startup and graph transport", type(error).__name__)

    else:
        print(f"  {WARN} Memory startup skipped until Bolt, chat and embeddings pass")

    if os.environ.get("MODULE") == "5" and s.nams_api_key:
        try:
            import httpx

            resp = httpx.get(
                f"{s.nams_base_url}/v1/conversations",
                headers={"Authorization": f"Bearer {s.nams_api_key}"},
                params={"limit": 1},
                timeout=15.0,
            )
            report(resp.status_code == 200, "NAMS key valid (module 5)", f"HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            report(False, "NAMS key valid (module 5)", type(exc).__name__)
    else:
        print(f"  {WARN} NAMS is optional here; validate separately for module 5")

    print(
        "\n"
        + (
            "All required checks passed. Try: make dev"
            if not failures
            else f"{failures} check(s) failed — resolve the failed checks and re-run make check"
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
