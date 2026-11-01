#!/usr/bin/env python3
"""Phase 0 spike 0.5 — LLM extraction on the locked release with the Acme Cloud
ontology (ADR 001 follow-up): ontology prompt rendering, typed relations,
forbidden-relation dropping, per-message latency."""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

SESSION = "spike-05"
MESSAGE = (
    "Hi, I'm Maya Chen — I work at Northwind Robotics, and we're on the Pro plan. "
    "The Acme Cloud Billing API charged us twice for Acme Cloud Compute."
)


async def main() -> None:
    from lib.settings import get_settings
    from module_3.app.memory import open_memory

    settings = get_settings()
    async with open_memory(settings, ontology="acme_cloud") as memory:
        assert memory is not None
        print("== SPIKE 0.5: LLM extraction + acme_cloud ontology ==")
        print(f"ontology resolved: {memory.ontology_document.domain.name}")
        print(f"validation_mode: {memory.validation_mode}")

        started = time.monotonic()
        await memory.short_term.add_message(SESSION, "user", MESSAGE)
        elapsed = time.monotonic() - started
        print(f"\nadd_message (with LLM extraction) latency: {elapsed:.2f}s")

        await asyncio.sleep(2)  # allow async bits to settle
        rows = await memory.query.cypher(
            "MATCH (e:Entity) RETURN labels(e) AS labels, e.name AS name, "
            "e.subtype AS subtype ORDER BY name"
        )
        print(f"\nentities extracted: {len(rows)}")
        for r in rows:
            print(f"  {r['name']}  {r['labels']}  subtype={r['subtype']}")

        rels = await memory.query.cypher(
            "MATCH (a:Entity)-[r:RELATED_TO]->(b:Entity) "
            "RETURN a.name AS src, r.type AS type, b.name AS tgt, "
            "r.support AS support, r.confidence AS conf"
        )
        print(f"typed relations: {len(rels)}")
        for r in rels:
            print(
                f"  {r['src']} -[{r['type']}]-> {r['tgt']} "
                f"(support={r['support']}, conf={r['conf']:.2f})"
            )
        undeclared = [
            r
            for r in rels
            if r["type"] not in {"WORKS_AT", "SUBSCRIBES_TO", "USES", "REPORTED", "AFFECTS"}
        ]
        print(f"undeclared (should-be-dropped) relations: {len(undeclared)}")
        mentions = await memory.query.cypher(
            "MATCH (m:Message)-[:MENTIONS]->(e:Entity) RETURN count(*) AS n"
        )
        print(f"MENTIONS edges: {mentions[0]['n']}")


if __name__ == "__main__":
    asyncio.run(main())
