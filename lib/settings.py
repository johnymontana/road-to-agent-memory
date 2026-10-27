"""Environment configuration. Env vars beat .env (ADR 003 secrets strategy)."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    # AuraDB (modules 1-4, Bolt backend)
    neo4j_uri: str = ""
    neo4j_username: str = "neo4j"
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"

    # OpenAI — chat, embeddings, LLM extraction (ADR 001)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # NAMS (module 5)
    nams_api_key: str = ""
    nams_base_url: str = "https://memory.neo4jlabs.com"

    # Workshop machinery
    module: int = 1
    ontology: str = "acme_cloud"  # or "default-poleo" (module 3 before/after beat)
    reasoning_retrieval: bool = True  # module 4 ablation flag (AGENT_REASONING_RETRIEVAL=off)
    data_dir: Path = ROOT / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "acme_cloud.db"

    @property
    def ontology_path(self) -> Path:
        return ROOT / "ontology" / f"{self.ontology}.yaml"


@lru_cache
def get_settings() -> AppSettings:
    module = os.environ.get("MODULE")
    retrieval = os.environ.get("AGENT_REASONING_RETRIEVAL")
    s = AppSettings()
    if module:
        s.module = int(module)
    if retrieval is not None:
        s.reasoning_retrieval = retrieval.lower() not in ("0", "off", "false")
    if o := os.environ.get("ONTOLOGY"):
        s.ontology = o
    # The neo4j-agent-memory OpenAI adapter and PydanticAI both read the raw
    # env var, not pydantic-settings — export it so .env-only setups work.
    if s.openai_api_key and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = s.openai_api_key
    return s
