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


async def search_entities(memory, query, embedding, namespace, customer_email=None):
    # Scope via source messages; expand employer relationships and expose the SQL
    # properties instead of only a lossy entity description.
    return await memory.query.cypher(
        """// workshop:entities
        MATCH (c:Conversation)-[:HAS_MESSAGE]->(:Message)-[:MENTIONS]->(e:Entity)
        WHERE c.session_id STARTS WITH $namespace
        OPTIONAL MATCH (e)-[:WORKS_AT]->(org:Entity)
        WITH DISTINCT e,org,
          CASE WHEN e.embedding IS NULL THEN 0.0
               ELSE vector.similarity.cosine(e.embedding,$embedding) END AS score
        WHERE ($customer_email IS NOT NULL AND e.email=$customer_email)
           OR toLower(coalesce(e.name,'')) CONTAINS toLower($query)
           OR toLower(coalesce(org.name,e.organization,'')) CONTAINS toLower($query)
           OR score >= 0.5
        RETURN e.id AS id,e.name AS name,e.type AS type,e.description AS description,
          e.email AS email,e.plan AS plan,e.signup_date AS signup_date,
          e.preferred_contact AS preferred_contact,e.organization AS organization,
          e.refund_limit AS refund_limit,e.hydrated_from AS source,score,
          org.name AS works_at
        ORDER BY CASE WHEN e.email=$customer_email THEN 0 ELSE 1 END,score DESC LIMIT 10""",
        {
            "query": query,
            "embedding": embedding,
            "namespace": namespace + ":",
            "customer_email": customer_email,
        },
    )


async def search_preferences(memory, customer_email, namespace):
    if not customer_email:
        return []
    return await memory.query.cypher(
        """// workshop:preferences
        MATCH (p:Preference)
        WHERE p.category STARTS WITH $category
        RETURN p.id AS id,p.preference AS preference,p.context AS context,p.category AS category
        ORDER BY p.created_at DESC LIMIT 10""",
        {"category": f"{namespace}:{customer_email}:"},
    )


async def build_context(
    memory, message, session_id, embedder, namespace, *, exclude_id=None, customer_email=None
):
    recent = await recent_messages(memory, session_id, exclude_id=exclude_id)
    embedding = await embedder.embed(message)
    semantic = await search_messages(memory, message, embedding, namespace, exclude_id=exclude_id)
    evidence = [{**r, "path": "recent_conversation"} for r in recent] + semantic
    entities = await search_entities(memory, message, embedding, namespace, customer_email)
    evidence += [{**r, "path": "grounded_entity"} for r in entities]
    preferences = await search_preferences(memory, customer_email, namespace)
    evidence += [{**r, "path": "customer_preference"} for r in preferences]
    return json.dumps(evidence, ensure_ascii=False, default=str), evidence
