#!/usr/bin/env python3
"""Minimal pinned-SDK Bolt write/retrieve recipe; uses .env and a unique conversation."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from neo4j_agent_memory import MemoryClient, MemorySettings

from lib.settings import get_settings


async def main():
    app = get_settings()
    settings = MemorySettings(
        backend="bolt",
        neo4j={
            "uri": app.neo4j_uri,
            "username": app.neo4j_username,
            "password": app.neo4j_password,
            "database": app.neo4j_database,
        },
        llm=f"openai/{app.openai_model}",
        embedding=f"openai/{app.embedding_model}",
        extraction={"extractor_type": "none"},
    )
    session = f"monday-{uuid4().hex}"
    async with MemoryClient(settings) as memory:
        phrase = "violet-" + uuid4().hex
        # add_message creates the (:Conversation) on first use and embeds the text.
        await memory.short_term.add_message(session, "user", f"My ticket phrase is {phrase}.")
        # The SDK's broad get_context also performs semantic retrieval across
        # conversations. Use an explicit session query for this scoped example.
        rows = await memory.query.cypher(
            "MATCH (:Conversation {session_id:$session})-[:HAS_MESSAGE]->(m:Message) "
            "RETURN m.id AS id,m.role AS role,m.content AS content "
            "ORDER BY m.timestamp DESC,m.id DESC LIMIT 10",
            {"session": session},
        )
        context = json.dumps(list(reversed(rows)))
        assert phrase in context and len(rows) == 1
        print(context)
        print(
            "Next: convert these rows to PydanticAI messages and pass them as "
            "agent.run(..., message_history=...). See as_model_history() in "
            "module_2/app/context.py."
        )


if __name__ == "__main__":
    asyncio.run(main())
