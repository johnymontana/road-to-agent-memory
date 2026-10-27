"""Command-surface tests (P1): the Makefile implements exactly the 29-target spec,
each target exists, and the help output lists them."""

from __future__ import annotations

import re
from pathlib import Path

from .command_surface_spec import CANONICAL_TARGETS

ROOT = Path(__file__).resolve().parent.parent
MAKEFILE = ROOT / "Makefile"


def makefile_targets() -> set[str]:
    text = MAKEFILE.read_text()
    targets = set()
    for match in re.finditer(r"^([a-zA-Z0-9][a-zA-Z0-9_-]*):[^=]", text, re.MULTILINE):
        targets.add(match.group(1))
    return targets


def test_all_canonical_targets_exist():
    implemented = makefile_targets()
    missing = [t for t in CANONICAL_TARGETS if t not in implemented]
    assert not missing, f"Makefile is missing canonical targets: {missing}"


def test_no_undeclared_targets():
    implemented = makefile_targets() - {"help"}  # help is the generated index
    extra = implemented - set(CANONICAL_TARGETS)
    assert not extra, f"Makefile has targets not in the spec: {sorted(extra)}"


def test_help_lists_every_target():
    text = MAKEFILE.read_text()
    help_block = text.split("help:")[1].split("\n\n")[0]
    for target in CANONICAL_TARGETS:
        assert target in help_block, f"make help does not list `{target}`"
