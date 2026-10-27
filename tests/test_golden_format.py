"""Golden-graph snapshot format (P3) + tolerance policy tests."""

from __future__ import annotations

import json
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"

REQUIRED_KEYS = {"scenario", "module", "exact", "aspirational"}


def test_golden_snapshots_conform():
    files = list(GOLDEN_DIR.glob("*.json"))
    assert files, "no golden snapshots committed yet (created at each module's Phase 3 exit)"
    for f in files:
        snap = json.loads(f.read_text())
        assert REQUIRED_KEYS <= snap.keys(), f"{f.name}: missing {REQUIRED_KEYS - snap.keys()}"
        # exact: assertions that must hold despite LLM extraction variance
        assert isinstance(snap["exact"].get("labels_present"), list)
        # aspirational: counts that may vary run-to-run
        assert isinstance(snap["aspirational"].get("entity_count_range"), list)
        assert len(snap["aspirational"]["entity_count_range"]) == 2
