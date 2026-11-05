"""Shared infrastructure for the Road to Agent Memory workshop modules.

Each module_N/ folder owns its agent and memory behavior; lib/ holds transport,
settings, SQL and graph serialization only (ADR 004).
"""

import logging
import os

# PydanticAI prints a multi-line observability banner on first use; it would
# interleave with scenario dialogue in participants' terminals.
os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")

# On a fresh graph, Neo4j warns about relationship types and properties that no
# memory has created yet (for example ABOUT before any preference is scoped).
# These notifications are expected and would only confuse workshop output.
logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)
