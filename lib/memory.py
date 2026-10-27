"""MemoryClient factory — memory capability grows with the module number.

Module 1: no memory client at all.
Module 2: short-term only (extraction disabled).
Module 3: + LLM extraction (ADR 001), active ontology, hydration, enrichment.
Module 4: + reasoning memory (traces recorded + similar-task retrieval).
Module 5: NAMS (hosted) — handled separately in lib/nams.py.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from neo4j_agent_memory import MemoryClient, MemorySettings, load_ontology
from neo4j_agent_memory.config.settings import SchemaConfig

from .settings import AppSettings


def build_settings(s: AppSettings, module: int) -> MemorySettings:
    extraction = (
        {"extractor_type": "none"}  # module 2: persistence only, extraction taught in 3
        if module < 3
        else {
            "extractor_type": "llm",  # ADR 001: structured outputs, temperature 0
        }
    )
    enrichment = None
    if module >= 3:
        # Wikipedia enrichment for real-world third parties (Stripe) — stretch beat.
        enrichment = {
            "enabled": True,
            "providers": ["wikimedia"],
            "entity_types": ["ORGANIZATION"],
        }
    kwargs: dict[str, Any] = {}
    if enrichment is not None:
        kwargs["enrichment"] = enrichment
    return MemorySettings(
        backend="bolt",
        neo4j={
            "uri": s.neo4j_uri,
            "username": s.neo4j_username,
            "password": s.neo4j_password,
            "database": s.neo4j_database,
        },
        llm=f"openai/{s.openai_model}",
        embedding=f"openai/{s.embedding_model}",
        extraction=extraction,
        # The Acme Cloud ontology is stored + activated in the DB by
        # scripts/activate_ontology.py (make module-3); clients pick it up at
        # connect time (F12: do NOT also set ontology_path — file config would
        # override the stored active version).
        schema_config=SchemaConfig(use_active_ontology=True),
        **kwargs,
    )


@asynccontextmanager
async def open_memory(
    s: AppSettings, module: int, ontology_path: Path | None = None
) -> AsyncIterator[MemoryClient | None]:
    """Yield a connected MemoryClient, or None for module 1 (stateless baseline)."""
    if module < 2:
        yield None
        return
    doc = load_ontology(str(ontology_path)) if ontology_path else None
    async with MemoryClient(build_settings(s, module), ontology=doc) as client:
        yield client
