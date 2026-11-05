"""Explicit best-effort public enrichment, cached with visible source/status."""

import hashlib
import json
import time

from neo4j_agent_memory.enrichment.wikimedia import WikimediaProvider

# Wikimedia rejects generic clients (HTTP 403, "robot policy"). Its User-Agent
# policy asks for a client name plus a contact URL: https://w.wiki/4wJS
USER_AGENT = (
    "road-to-agent-memory-workshop/1.0 (https://github.com/johnymontana/road-to-agent-memory)"
)


async def enrich_organization(settings, name="Stripe, Inc.", *, provider=None, refresh=False):
    folder = settings.data_dir / "enrichment-cache"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (hashlib.sha256(name.casefold().encode()).hexdigest() + ".json")
    if path.exists() and not refresh:
        cached = json.loads(path.read_text())
        ttl = 604800 if cached["status"] == "success" else 300
        if time.time() - cached["retrieved_at"] < ttl:
            return {**cached, "cached": True}
    try:
        result = await (provider or WikimediaProvider(user_agent=USER_AGENT)).enrich(
            name, "ORGANIZATION"
        )
        status = getattr(result.status, "value", str(result.status)).lower()
        data = {
            "name": name,
            "status": status,
            "provider": "wikimedia",
            "retrieved_at": time.time(),
            "enriched_description": result.description,
            "wikipedia_url": result.wikipedia_url,
            "error": result.error_message,
            "cached": False,
            "live": True,
        }
    except Exception as error:
        data = {
            "name": name,
            "status": "unavailable",
            "provider": "wikimedia",
            "retrieved_at": time.time(),
            "error": type(error).__name__,
            "cached": False,
            "live": True,
        }
    path.write_text(json.dumps(data, indent=2))
    snapshot = {
        "id": f"enrichment-{path.stem[:12]}",
        "title": f"Wikimedia {name} · {data['status']}",
        "module": 3,
        "protocol": "Optional public organization enrichment, not operational status.",
        "graph": {
            "nodes": [
                {"id": "organization", "labels": ["Entity", "Organization"], "properties": data}
            ],
            "relationships": [],
            "truncated": False,
        },
    }
    replay = settings.data_dir / "replays"
    replay.mkdir(parents=True, exist_ok=True)
    (replay / f"{snapshot['id']}.json").write_text(json.dumps(snapshot, indent=2))
    return data
