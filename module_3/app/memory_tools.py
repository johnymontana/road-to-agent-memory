"""Memory tools: the model can search memory and save preferences on its own.

context.py retrieves memory *before* every turn. These tools let the model look
again mid-turn with its own query, and write a customer preference when asked.
They have the same names as `neo4j_agent_memory.integrations.pydantic_ai
.create_memory_tools()`. This version is scoped to the workshop namespace and to
the customer the operator selected, and records each call for the trace panel.
"""

from __future__ import annotations

import json
import time

from pydantic_ai import RunContext

from .context import customer_id, search_entities, search_messages, search_preferences
from .tools import ToolDeps, _record


def create_memory_tools(memory):
    async def search_memory(ctx: RunContext[ToolDeps], query: str) -> str:
        """Search earlier statements, known customers and their employers. Cite IDs."""
        started = time.monotonic()
        deps = ctx.deps
        embedding = await deps.embedder.embed(query)
        found = {
            "messages": await search_messages(
                memory, query, embedding, deps.namespace, exclude_id=deps.current_message_id
            ),
            "entities": await search_entities(
                memory, query, embedding, deps.namespace, deps.account_email
            ),
            "preferences": await search_preferences(memory, deps.account_email, deps.namespace),
        }
        return _record(
            ctx, "search_memory", {"query": query}, None, started, json.dumps(found, default=str)
        )

    async def save_preference(
        ctx: RunContext[ToolDeps], category: str, preference: str, context: str | None = None
    ) -> str:
        """Save a preference for the selected customer, e.g. category "contact"."""
        started = time.monotonic()
        deps = ctx.deps
        if not deps.account_email:
            saved = {"status": "needs_customer", "reason": "Select a customer before saving"}
        else:
            user = customer_id(deps.namespace, deps.account_email)
            stored = await memory.long_term.add_preference(
                # The library deduplicates similar preferences *within a category*,
                # across all users. Prefixing the category with the customer keeps
                # one customer's preference from merging into another's.
                f"{user}:{category}",
                preference,
                context=context,
                user_identifier=user,  # Writes (:User)-[:HAS_PREFERENCE]->(:Preference).
            )
            saved = {
                "status": "stored",
                "id": str(stored.id),
                "category": stored.category,
                "preference": stored.preference,
                "context": stored.context,
                "deduplicated": bool(stored.metadata.get("deduplicated", False)),
            }
        return _record(
            ctx,
            "save_preference",
            {"category": category, "preference": preference, "context": context},
            None,
            started,
            json.dumps(saved),
        )

    async def recall_preferences(ctx: RunContext[ToolDeps]) -> str:
        """Recall the selected customer's stored preferences and when they apply."""
        started = time.monotonic()
        deps = ctx.deps
        rows = await search_preferences(memory, deps.account_email, deps.namespace)
        return _record(ctx, "recall_preferences", {}, None, started, json.dumps(rows, default=str))

    return [search_memory, save_preference, recall_preferences]
