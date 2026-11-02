"""Module 5's explicit Bolt memory configuration. Read alongside agent.py."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from neo4j_agent_memory import MemoryClient, MemorySettings, load_ontology
from neo4j_agent_memory.config.settings import SchemaConfig

from lib.settings import AppSettings

ONTOLOGY_DIR = Path(__file__).resolve().parents[1] / "ontology"


def build_settings(settings: AppSettings) -> MemorySettings:
    return MemorySettings(
        backend="bolt",
        neo4j={
            "uri": settings.neo4j_uri,
            "username": settings.neo4j_username,
            "password": settings.neo4j_password,
            "database": settings.neo4j_database,
            "connection_timeout": 10,
            "max_transaction_retry_time": 5,
        },
        llm=f"openai/{settings.openai_model}",
        embedding=f"openai/{settings.embedding_model}",
        extraction={"extractor_type": "llm"},
        enrichment={"enabled": False},  # Explicit, cached optional workflow only.
        schema_config=SchemaConfig(
            use_active_ontology=True, validation_mode=settings.validation_mode
        ),
    )


@asynccontextmanager
async def open_memory(settings: AppSettings, *, ontology: str | None = None):
    """Select this lesson's ontology; 'active' uses the version stored in AuraDB.

    An explicit file wins over the active database version. Default/custom
    comparisons pass a selection per invocation, without changing global state.
    """
    selection = ontology or settings.ontology
    document = None
    if selection != "active":
        if selection not in ("acme_cloud", "default-poleo"):
            raise ValueError("ontology must be acme_cloud, default-poleo, or active")
        document = load_ontology(str(ONTOLOGY_DIR / f"{selection}.yaml"))
    source = (
        "database active ontology"
        if selection == "active"
        else str(ONTOLOGY_DIR / f"{selection}.yaml")
    )
    print(f"Module 5 ontology source: {source}; validation={settings.validation_mode}", flush=True)
    async with MemoryClient(build_settings(settings), ontology=document) as memory:
        yield memory
