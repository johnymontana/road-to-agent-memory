"""Graph endpoints: map Neo4j (Bolt) and NAMS (REST) graph state to the NVL shape
defined in docs/frontend-contract.md."""

from __future__ import annotations

from typing import Any

import httpx
from neo4j_agent_memory import MemoryClient

from .settings import AppSettings

_LAYER_LABELS = {
    "short_term": ["Conversation", "Message"],
    "long_term": ["Entity", "Preference", "Fact"],
    "reasoning": ["ReasoningTrace", "ReasoningStep", "ToolCall", "Tool"],
}


def _labels_for_layer(layer: str) -> list[str]:
    return _LABELS_FOR_ALL if layer == "all" else _LAYER_LABELS.get(layer, _LABELS_FOR_ALL)


_LABELS_FOR_ALL = [lbl for labels in _LAYER_LABELS.values() for lbl in labels]


def _json_value(value):
    if isinstance(value, dict):
        return {k: _json_value(v) for k, v in value.items() if "embedding" not in k.lower()}
    if isinstance(value, (list, tuple)):
        return [_json_value(v) for v in value]
    if hasattr(value, "iso_format"):
        return value.iso_format()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


async def bolt_graph(
    client: MemoryClient,
    layer: str = "all",
    *,
    session_id: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Return bounded, induced graph maps, never serialized driver objects."""
    labels = _labels_for_layer(layer)
    rows = await client.query.cypher(
        """
        MATCH (n)
        WHERE any(l IN labels(n) WHERE l IN $labels)
          AND ($session_id IS NULL OR n.session_id = $session_id
            OR EXISTS {
              MATCH (c:Conversation {session_id: $session_id})-[:HAS_MESSAGE]->(msg)
              WHERE n = c OR n = msg OR (msg)-[:MENTIONS]->(n)
            }
            OR EXISTS {
              MATCH (t:ReasoningTrace {session_id: $session_id})-[:HAS_STEP*0..1]->(s)
              WHERE n = s OR (s)-[:USES_TOOL]->(n) OR (s)-[:TOUCHED]->(n)
                OR EXISTS { MATCH (s)-[:USES_TOOL]->(:ToolCall)-[:INSTANCE_OF]->(n) }
            }
            OR (n:Preference AND $session_id IS NOT NULL AND
                n.category STARTS WITH $preference_namespace)
            OR EXISTS {
              MATCH (:Conversation {session_id: $session_id})-[:HAS_MESSAGE]->(:Message)
                -[:MENTIONS]->(e)<-[:ABOUT]-(n:Preference)
              WHERE n.category STARTS WITH $preference_namespace
            })
        WITH n ORDER BY coalesce(n.timestamp, n.created_at, n.started_at) DESC,
                        elementId(n)
        LIMIT $limit
        WITH collect(n) AS candidates
        WITH candidates[..$visible_limit] AS chosen,
             size(candidates) > $visible_limit AS truncated
        UNWIND chosen AS n
        OPTIONAL MATCH (n)-[r]->(m) WHERE m IN chosen
        RETURN {id: elementId(n), labels: labels(n), properties: properties(n)} AS n,
          CASE WHEN m IS NULL THEN null ELSE
            {id: elementId(m), labels: labels(m), properties: properties(m)} END AS m,
          CASE WHEN r IS NULL THEN null ELSE
            {id: elementId(r), from: elementId(startNode(r)),
             to: elementId(endNode(r)), type: type(r), properties: properties(r)} END AS r,
          truncated
        """,
        {
            "labels": labels,
            "session_id": session_id,
            "limit": limit + 1,
            "visible_limit": limit,
            "preference_namespace": (session_id or "").split(":")[0] + ":",
        },
    )
    nodes = {}
    relationships = {}
    for row in rows:
        for key in ("n", "m"):
            node = row.get(key)
            if node:
                nodes[str(node["id"])] = _json_value(node)
        relationship = row.get("r")
        if relationship:
            relationships[str(relationship["id"])] = _json_value(relationship)
    return {
        "nodes": list(nodes.values()),
        "relationships": list(relationships.values()),
        "truncated": any(r.get("truncated", False) for r in rows),
        "session_id": session_id,
    }


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
