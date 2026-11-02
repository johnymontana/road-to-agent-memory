"""Lesson-owned context: scoped evidence, explicit retrieval paths, newest history."""

from __future__ import annotations

import json


async def recent_messages(memory, session_id, *, exclude_id=None):
    rows = await memory.query.cypher(
        """// workshop:recent
        MATCH (:Conversation {session_id:$session_id})-[:HAS_MESSAGE]->(m:Message)
        WHERE $exclude_id IS NULL OR m.id <> $exclude_id
        RETURN m.id AS id,m.role AS role,m.content AS content
        ORDER BY m.timestamp DESC,m.id DESC LIMIT 10""",
        {"session_id": session_id, "exclude_id": exclude_id},
    )
    return list(reversed(rows))


async def search_messages(memory, query, embedding, namespace, *, exclude_id=None):
    rows = await memory.query.cypher(
        """// workshop:semantic
        MATCH (c:Conversation)-[:HAS_MESSAGE]->(m:Message)
        WHERE c.session_id STARTS WITH $namespace AND m.id <> coalesce($exclude_id,'')
          AND m.role='user' AND m.embedding IS NOT NULL
          AND toLower(m.content) <> toLower($query)
        WITH m,c,vector.similarity.cosine(m.embedding,$embedding) AS score
        WHERE score >= 0.5
        RETURN m.id AS id,m.role AS role,m.content AS content,
               c.session_id AS session_id,score
        ORDER BY score DESC LIMIT 40""",
        {
            "namespace": namespace + ":",
            "exclude_id": exclude_id,
            "embedding": embedding,
            "query": query,
        },
    )
    seen = set()
    evidence = []
    for row in rows:
        text = row["content"].strip()
        key = text.casefold()
        if key in seen or key.startswith(
            ("do you remember", "what did we", "what is my", "who is", "how long")
        ):
            continue
        seen.add(key)
        evidence.append({**row, "path": "semantic_message"})
        if len(evidence) == 5:
            break
    return evidence


async def build_context(
    memory, message, session_id, embedder, namespace, *, exclude_id=None, customer_email=None
):
    recent = await recent_messages(memory, session_id, exclude_id=exclude_id)
    embedding = await embedder.embed(message)
    semantic = await search_messages(memory, message, embedding, namespace, exclude_id=exclude_id)
    evidence = [{**r, "path": "recent_conversation"} for r in recent] + semantic
    return json.dumps(evidence, ensure_ascii=False, default=str), evidence
