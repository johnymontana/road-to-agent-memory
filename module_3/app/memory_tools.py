"""Local memory tools expose grounded fields and actual stored preference receipts."""

from __future__ import annotations

import json
import time

from pydantic_ai import RunContext

from .context import search_entities, search_messages, search_preferences
from .tools import ToolDeps, _record


def create_memory_tools(memory):
    async def search_memory(ctx: RunContext[ToolDeps], query: str) -> str:
        """Search scoped statements, customer facts and employer relationships. Cite IDs."""
        start = time.monotonic()
        d = ctx.deps
        embedding = await d.embedder.embed(query)
        messages = await search_messages(
            memory, query, embedding, d.namespace, exclude_id=d.current_message_id
        )
        entities = await search_entities(memory, query, embedding, d.namespace, d.account_email)
        preferences = await search_preferences(memory, d.account_email, d.namespace)
        data = {"messages": messages, "entities": entities, "preferences": preferences}

        return _record(
            ctx, "search_memory", {"query": query}, None, start, json.dumps(data, default=str)
        )

    async def save_preference(
        ctx: RunContext[ToolDeps], category: str, preference: str, context: str | None = None
    ) -> str:
        """Save a preference for the explicitly selected customer, never the whole workspace."""
        start = time.monotonic()
        d = ctx.deps
        if not d.account_email:
            out = {
                "status": "needs_customer",
                "reason": "Select a customer before saving preferences",
            }
        else:
            scoped = f"{d.namespace}:{d.account_email}:{category}"
            saved = await memory.long_term.add_preference(
                scoped,
                preference,
                context=context,
                user_identifier=f"{d.namespace}:{d.account_email}",
            )
            out = {
                "status": "stored",
                "id": str(saved.id),
                "category": saved.category,
                "preference": saved.preference,
                "context": saved.context,
                "deduplicated": bool(saved.metadata.get("deduplicated", False)),
            }
        return _record(
            ctx,
            "save_preference",
            {"category": category, "preference": preference, "context": context},
            None,
            start,
            json.dumps(out),
        )

    async def recall_preferences(ctx: RunContext[ToolDeps], topic: str) -> str:
        """Recall only the selected customer's preferences, including applicability context."""
        start = time.monotonic()
        d = ctx.deps
        rows = await search_preferences(memory, d.account_email, d.namespace)
        return _record(
            ctx, "recall_preferences", {"topic": topic}, None, start, json.dumps(rows, default=str)
        )

    return [search_memory, save_preference, recall_preferences]
