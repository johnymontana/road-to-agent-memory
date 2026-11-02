"""Environment configuration. Env vars beat .env (ADR 003 secrets strategy)."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    # AuraDB (memory-enabled support agents in modules 2-5, Bolt backend)
    neo4j_uri: str = ""
    neo4j_username: str = "neo4j"
    neo4j_password: str = Field(default="", repr=False)
    neo4j_database: str = "neo4j"

    # OpenAI — chat, embeddings, LLM extraction (ADR 001)
    openai_api_key: str = Field(default="", repr=False)
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # NAMS (module 5)
    nams_api_key: str = Field(default="", repr=False)
    nams_base_url: str = "https://memory.neo4jlabs.com"

    # Workshop machinery
    data_dir: Path = ROOT / "data"
    memory_namespace: str = "workshop"
    ontology: str = "acme_cloud"
    agent_reasoning_retrieval: bool = True
    validation_mode: Literal["permissive", "strict"] = "permissive"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "acme_cloud.db"


@lru_cache
def get_settings() -> AppSettings:
    s = AppSettings()
    # The neo4j-agent-memory OpenAI adapter and PydanticAI both read the raw
    # env var, not pydantic-settings — export it so .env-only setups work.
    if s.openai_api_key and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = s.openai_api_key
    return s
