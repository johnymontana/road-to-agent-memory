"""Behavioral lane (P3): run scenarios against an ephemeral Neo4j and compare
the resulting subgraph to the committed golden snapshot with tolerances.

Skipped unless RUN_BEHAVIORAL=1 and OPENAI_API_KEY is set — CI runs this lane
on schedule (weekly re-verification) and on demand; it is not a per-PR gate
because it spends real LLM tokens.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "tests" / "golden"

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_BEHAVIORAL") != "1" or not os.environ.get("OPENAI_API_KEY"),
    reason="behavioral lane: set RUN_BEHAVIORAL=1 and OPENAI_API_KEY (weekly CI or manual)",
)


def compare_to_golden(snapshot_name: str, observed: dict) -> list[str]:
    """Return a list of violations (empty = pass). Tolerances per Phase 2.7."""
    golden_path = GOLDEN / f"{snapshot_name}.json"
    if not golden_path.exists():
        pytest.skip(f"no golden snapshot for {snapshot_name} yet")
    golden = json.loads(golden_path.read_text())
    violations = []
    for label in golden["exact"].get("labels_present", []):
        if label not in observed["labels"]:
            violations.append(f"missing required label: {label}")
    lo, hi = golden["aspirational"]["entity_count_range"]
    if not lo <= observed["entity_count"] <= hi:
        violations.append(
            f"entity_count {observed['entity_count']} outside range [{lo}, {hi}]"
        )
    return violations


@pytest.mark.behavioral
async def test_placeholder_behavioral_lane():
    """Replaced at each module's Phase 3 exit with scenario runs against
    testcontainers Neo4j: run scenario → dump subgraph → compare_to_golden."""
    pytest.skip("behavioral scenarios land with Phase 3 module exits")
