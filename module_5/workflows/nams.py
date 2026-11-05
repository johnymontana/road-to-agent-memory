"""Shared plumbing for the module 5 workflows: an authenticated NAMS client and
the files that pass state from one make target to the next.

neo4j-agent-memory has no client for the NAMS skills API yet, so these are plain
HTTP calls against https://memory.neo4jlabs.com/openapi.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "artifacts" / "distilled"  # SKILL.md, references/, provenance.json
SKILL_NAME = "acme-refund-procedure"


def client(settings) -> httpx.AsyncClient:
    if not settings.nams_api_key:
        sys.exit("NAMS_API_KEY not set. Add it to .env, then run make nams-check.")
    return httpx.AsyncClient(
        base_url=settings.nams_base_url,
        headers={"Authorization": f"Bearer {settings.nams_api_key}"},
        timeout=60.0,
    )


async def call(http: httpx.AsyncClient, method: str, path: str, body=None) -> dict:
    """One request; on an error, show NAMS's own explanation before raising."""
    response = await http.request(method, path, json=body)
    if response.is_error:
        print(f"NAMS {method} {path} → HTTP {response.status_code}: {response.text[:300]}")
    response.raise_for_status()
    return response.json() if response.content else {}


def seed_state_path(settings) -> Path:
    """Written by nams-seed: the seeded conversation, which scopes distillation."""
    return Path(settings.data_dir) / "nams-workspace.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
