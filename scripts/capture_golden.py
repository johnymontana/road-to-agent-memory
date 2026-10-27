#!/usr/bin/env python3
"""Capture a golden-graph snapshot from the CURRENT memory state (Phase 3 exit
criterion per module). Writes tests/golden/<name>.json with exact assertions
and aspirational tolerances. Usage: uv run scripts/capture_golden.py m4-state"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
GOLDEN = ROOT / "tests" / "golden"

ONT_LABELS = ["Customer", "Organization", "Product", "Plan", "Incident"]
REASONING_LABELS = ["ReasoningTrace", "ReasoningStep", "ToolCall"]


async def main(name: str) -> None:
    from lib.memory import open_memory
    from lib.settings import get_settings

    settings = get_settings()
    async with open_memory(settings, 4) as memory:
        assert memory is not None
        labels = await memory.query.cypher(
            "MATCH (n) UNWIND labels(n) AS l RETURN DISTINCT l AS label ORDER BY l"
        )
        entity_count = (
            await memory.query.cypher("MATCH (e:Entity) RETURN count(e) AS n")
        )[0]["n"]
        rel_types = await memory.query.cypher(
            "MATCH ()-[r]->() RETURN DISTINCT type(r) AS t ORDER BY t"
        )
        traces = (
            await memory.query.cypher(
                "MATCH (t:ReasoningTrace) RETURN count(t) AS n, "
                "sum(CASE WHEN t.success = false THEN 1 ELSE 0 END) AS failed"
            )
        )[0]

    snapshot = {
        "scenario": name,
        "module": 4,
        "generated_by": "scripts/capture_golden.py — regenerate at each module's Phase 3 exit",
        "exact": {
            "labels_present": [r["label"] for r in labels],
            "relationship_types": [r["t"] for r in rel_types],
            "trace_count": traces["n"],
            "failed_trace_count": traces["failed"],
        },
        "aspirational": {
            "entity_count_range": [max(0, entity_count - 3), entity_count + 3],
        },
    }
    path = GOLDEN / f"{name}.json"
    path.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"wrote {path}")
    print(f"  labels: {snapshot['exact']['labels_present']}")
    print(f"  relationships: {snapshot['exact']['relationship_types']}")
    print(f"  entities: {entity_count} (±3), traces: {traces['n']} "
          f"({traces['failed']} failed)")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "m4-state"))
