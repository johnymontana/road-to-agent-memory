"""Immutable extractor-only comparisons. No graph, SQL, or conversation mutation."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from uuid import uuid4

from neo4j_agent_memory import load_ontology
from neo4j_agent_memory.extraction.llm_extractor import LLMEntityExtractor

from lib.settings import AppSettings

TRANSCRIPT = (
    "Maya Chen works at Northwind Robotics and subscribes to the Pro plan. "
    "Maya uses Acme Cloud Compute and Acme Cloud Billing API. "
    "Maya reported incident BILL-104: a duplicate charge affecting Acme Cloud Compute. "
    "Maya calls the vendor AcmeCloud, also known as Acme Cloud."
)
ONTOLOGY_DIR = Path(__file__).resolve().parents[1] / "ontology"


async def run_extraction_snapshot(settings: AppSettings, ontology_name: str, *, extractor=None):
    if ontology_name not in ("acme_cloud", "default-poleo"):
        raise ValueError("Unknown comparison ontology")
    ontology = load_ontology(str(ONTOLOGY_DIR / f"{ontology_name}.yaml"))
    extractor = extractor or LLMEntityExtractor(
        model=f"openai/{settings.openai_model}",
        api_key=settings.openai_api_key,
        ontology=ontology,
        temperature=0,
    )
    start = time.monotonic()
    result = (await extractor.extract(TRANSCRIPT)).filter_invalid_entities(ontology)
    result, dropped = result.validate_relations(ontology, mode="drop")
    identifier = f"ontology-{ontology_name}-{uuid4().hex[:10]}"
    nodes = [
        {
            "id": "source",
            "labels": ["Message"],
            "properties": {"content": TRANSCRIPT, "source": "fixed transcript", "immutable": True},
        }
    ]
    rels = []
    by_name = {}
    by_mention = {}
    omitted = []
    for index, entity in enumerate(result.entities):
        node_id = f"entity-{index}"
        label = ontology.node_label(entity.type, entity.subtype) or entity.type.title()
        nodes.append(
            {
                "id": node_id,
                "labels": ["Entity", label],
                "properties": {
                    "name": entity.name,
                    "type": entity.type,
                    "subtype": entity.subtype,
                    "source": "LLM extractor",
                    "confidence": entity.confidence,
                },
            }
        )
        by_name.setdefault(entity.name.casefold(), []).append(node_id)
        if entity.id:
            by_mention.setdefault(entity.id, []).append(node_id)
        rels.append(
            {
                "id": f"mention-{index}",
                "from": "source",
                "to": node_id,
                "type": "MENTIONS",
                "properties": {"source": "fixed transcript"},
            }
        )
    for index, relation in enumerate(result.relations):

        def endpoint(mention_id, name):
            candidates = (
                by_mention.get(mention_id, []) if mention_id else by_name.get(name.casefold(), [])
            )
            return candidates[0] if len(candidates) == 1 else None

        source = endpoint(relation.source_id, relation.source)
        target = endpoint(relation.target_id, relation.target)
        if not source or not target:
            omitted.append(
                {"relation": relation.model_dump(), "reason": "missing or ambiguous endpoint"}
            )
        if source and target:
            rels.append(
                {
                    "id": f"relation-{index}",
                    "from": source,
                    "to": target,
                    "type": relation.relation_type,
                    "properties": {"confidence": relation.confidence},
                }
            )
    snapshot = {
        "id": identifier,
        "title": f"Extractor only · {ontology_name}",
        "module": 3,
        "protocol": (
            "Fixed transcript; independent extractor call; no chat history, "
            "hydration or graph merging."
        ),
        "transcript_sha256": hashlib.sha256(TRANSCRIPT.encode()).hexdigest(),
        "model": settings.openai_model,
        "ontology": ontology_name,
        "seconds": round(time.monotonic() - start, 3),
        "raw_extraction": result.model_dump(),
        "dropped_relations": [r.model_dump() for r in dropped],
        "omitted_ambiguous_relations": omitted,
        "graph": {"nodes": nodes, "relationships": rels, "truncated": False},
    }
    folder = settings.data_dir / "replays"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{identifier}.json").write_text(json.dumps(snapshot, indent=2))
    return snapshot
