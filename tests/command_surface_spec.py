"""The canonical command surface — 29 targets (P1 fix).

This list is the machine-readable mirror of WORKSHOP_OUTLINE.md's Makefile
spec table. tests/test_command_surface.py verifies the Makefile implements
exactly this set, so documents and implementation can't drift apart.
"""

SETUP = ["setup", "check", "seed", "dev"]
MODULES = [f"module-{n}" for n in range(6)]
SCENARIOS = [
    "s1-baseline",
    "s2-return",
    "s2-restart",
    "s3-default",
    "s3-ontology",
    "s3-enrich",
    "s4-refund",
    "s4-refund-repeat",
    "s4-fail",
    "s5-fresh-agent",
]
NAMS = [
    "nams-check",
    "nams-seed",
    "nams-distill",
    "nams-drift",
    "policy-change",
    "nams-redistill",
]
UTILITIES = ["eval", "reset-memory", "clean"]

CANONICAL_TARGETS = SETUP + MODULES + SCENARIOS + NAMS + UTILITIES
assert len(CANONICAL_TARGETS) == 29
