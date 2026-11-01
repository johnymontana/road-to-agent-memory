"""Agent-facing memory tools, including their visible tool-call evidence."""

from __future__ import annotations

import time

from neo4j_agent_memory import MemoryClient
from pydantic_ai import RunContext

from .tools import ToolDeps, _record


def create_memory_tools(memory: MemoryClient, *, reasoning_retrieval: bool = True) -> list:
    async def search_memory(ctx: RunContext[ToolDeps], query: str) -> str:
        """Search persistent conversations, grounded customer facts, and preferences.

        Call this first when a returning customer asks about themselves or history.
        """
        started = time.monotonic()
        lines = []
        for message in await memory.short_term.search_messages(query, limit=5):
            role = getattr(message.role, "value", message.role)
            lines.append(f"[{role}] {message.content}")
        for entity in await memory.long_term.search_entities(query, limit=5):
            lines.append(f"[ENTITY] {entity.name}: {entity.description or ''}")
        for preference in await memory.long_term.search_preferences(query, limit=5):
            lines.append(f"[PREFERENCE:{preference.category}] {preference.preference}")
        # Respect the ablation here too: tools cannot silently re-enable retrieval.
        if reasoning_retrieval:
            for trace in await memory.reasoning.get_similar_traces(
                query, limit=3, success_only=False
            ):
                status = "succeeded" if trace.success else "failed"
                lines.append(f"[TASK] {trace.task} - {status}: {trace.outcome or ''}")
        out = "\n".join(lines) or "No relevant memories found."
        return _record(ctx, "search_memory", {"query": query}, None, started, out)

    async def save_preference(
        ctx: RunContext[ToolDeps], category: str, preference: str, context: str | None = None
    ) -> str:
        """Save a support preference, such as email rather than phone follow-ups."""
        started = time.monotonic()
        await memory.long_term.add_preference(category, preference, context=context)
        return _record(
            ctx,
            "save_preference",
            {"category": category, "preference": preference, "context": context},
            None,
            started,
            f"Saved preference: {preference} (category: {category})",
        )

    async def recall_preferences(ctx: RunContext[ToolDeps], topic: str) -> str:
        """Recall preferences relevant to a support topic."""
        started = time.monotonic()
        preferences = await memory.long_term.search_preferences(topic, limit=10)
        out = "\n".join(f"[{p.category}] {p.preference}" for p in preferences)
        return _record(
            ctx,
            "recall_preferences",
            {"topic": topic},
            None,
            started,
            out or "No preferences found for this topic.",
        )

    return [search_memory, save_preference, recall_preferences]
