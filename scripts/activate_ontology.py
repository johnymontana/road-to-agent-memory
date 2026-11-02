#!/usr/bin/env python3
"""Store + activate an ontology in the database (module 3).

After activation, every client with use_active_ontology=True picks it up at
connect time. F12 pitfall: if the app was configured with ontology_path, unset
it — a file config overrides the stored active version.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


async def main(path: str) -> None:
    from neo4j_agent_memory import MemoryClient, load_ontology

    from lib.settings import get_settings
    from module_3.app.memory import build_settings

    s = get_settings()
    doc = load_ontology(path)
    async with MemoryClient(build_settings(s)) as client:
        version = await client.ontology.create(doc.domain.name, doc, validation_mode="permissive")
        await client.ontology.activate(version.id)
        print(f"Ontology '{doc.domain.name}' stored and activated (version {version.id}).")
        print("Entity types:", ", ".join(e.label for e in doc.entity_types))
        print("Relationships:", ", ".join(sorted({r.type for r in doc.relationships})))
    print(
        "\nSelect ONTOLOGY=active, then restart make dev MODULE=3. Local "
        "YAML is the default override."
    )


if __name__ == "__main__":
    default = ROOT / "module_3" / "ontology" / "acme_cloud.yaml"
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else str(default)))
