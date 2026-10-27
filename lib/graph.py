"""Graph endpoints: map Neo4j (Bolt) and NAMS (REST) graph state to the NVL shape
defined in docs/frontend-contract.md."""

from __future__ import annotations

from typing import Any

import httpx
from neo4j_agent_memory import MemoryClient

from .settings import AppSettings

_LAYER_LABELS = {
    "short_term": ["Conversation", "Message"],
    "long_term": ["Entity"],
    "reasoning": ["ReasoningTrace", "ReasoningStep", "ToolCall", "Tool"],
}


def _labels_for_layer(layer: str) -> list[str]:
    return _LABELS_FOR_ALL if layer == "all" else _LAYER_LABELS.get(layer, _LABELS_FOR_ALL)


_LABELS_FOR_ALL = [lbl for labels in _LAYER_LABELS.values() for lbl in labels]


async def bolt_graph(client: MemoryClient, layer: str = "all") -> dict[str, Any]:
    labels = _labels_for_layer(layer)
    rows = await client.query.cypher(
        """
        MATCH (n)
        WHERE any(l IN labels(n) WHERE l IN $labels)
        OPTIONAL MATCH (n)-[r]-(m)
        WHERE any(l IN labels(m) WHERE l IN $labels)
        RETURN n, r, m
        LIMIT 500
        """,
        {"labels": labels},
    )
    nodes: dict[str, dict] = {}
    rels: dict[str, dict] = {}

    def add_node(node) -> None:
        nid = str(node.element_id)
        props = {k: v for k, v in dict(node).items() if k != "embedding"}
        nodes[nid] = {"id": nid, "labels": list(node.labels), "properties": props}

    for row in rows:
        add_node(row["n"])
        if row["m"] is not None:
            add_node(row["m"])
        if row["r"] is not None:
            r = row["r"]
            rid = str(r.element_id)
            rels[rid] = {
                "id": rid,
                "from": str(r.start_node.element_id),
                "to": str(r.end_node.element_id),
                "type": r.type,
                "properties": dict(r),
            }
    return {"nodes": list(nodes.values()), "relationships": list(rels.values())}


async def nams_graph(s: AppSettings) -> dict[str, Any]:
    """Skill subgraph from the NAMS workspace (module 5) via read-only Cypher REST."""
    if not s.nams_api_key:
        return {"nodes": [], "relationships": [], "unavailable": True}
    try:
        async with httpx.AsyncClient(
            base_url=s.nams_base_url,
            headers={"Authorization": f"Bearer {s.nams_api_key}"},
            timeout=30.0,
        ) as http:
            resp = await http.post(
                "/v1/query",
                json={
                    "cypher": (
                        "MATCH (n) WHERE any(l IN labels(n) WHERE l STARTS WITH 'Skill') "
                        "OPTIONAL MATCH (n)-[r]-(m) RETURN n, r, m LIMIT 300"
                    )
                },
            )
            resp.raise_for_status()
            payload = resp.json()
    except httpx.HTTPError:
        return {"nodes": [], "relationships": [], "unavailable": True}

    # NAMS /v1/query returns {columns, rows}; rows contain node maps with
    # element id / labels / properties depending on deployment — map defensively.
    nodes: dict[str, dict] = {}
    rels: dict[str, dict] = {}
    for row in payload.get("rows", []):
        record = dict(zip(payload.get("columns", []), row, strict=False))
        for key in ("n", "m"):
            node = record.get(key)
            if isinstance(node, dict) and node.get("id") is not None:
                nid = str(node["id"])
                nodes[nid] = {
                    "id": nid,
                    "labels": node.get("labels", []),
                    "properties": node.get("properties", node),
                }
        rel = record.get("r")
        if isinstance(rel, dict) and rel.get("id") is not None:
            rid = str(rel["id"])
            rels[rid] = {
                "id": rid,
                "from": str(rel.get("from") or rel.get("start")),
                "to": str(rel.get("to") or rel.get("end")),
                "type": rel.get("type", "RELATED"),
                "properties": rel.get("properties", {}),
            }
    return {"nodes": list(nodes.values()), "relationships": list(rels.values())}
