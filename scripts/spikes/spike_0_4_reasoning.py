#!/usr/bin/env python3
"""Phase 0 spike 0.4 — Bolt reasoning memory (F7): record_agent_trace with a
real AgentRunResult (PydanticAI's built-in test model — no token spend),
similar-trace retrieval, and :TOUCHED edges."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

SESSION = "spike-04"
TASK = "Refund duplicate $49 Acme Cloud Compute charge for Maya Chen"


async def main() -> None:
    from neo4j_agent_memory.integrations.pydantic_ai import record_agent_trace
    from pydantic_ai import Agent

    from lib.settings import get_settings
    from module_4.app.memory import open_memory

    settings = get_settings()
    async with open_memory(settings) as memory:
        assert memory is not None

        # A real agent run on the built-in test model (free, deterministic).
        agent = Agent("test", output_type=str, tools=[lambda: "Pro plan, refund limit $250"])
        result = await agent.run("process the refund")

        print("== record_agent_trace ==")
        import inspect

        print(f"is coroutine function: {inspect.iscoroutinefunction(record_agent_trace)}")
        trace = await record_agent_trace(
            memory.reasoning, session_id=SESSION, result=result, task=TASK
        )
        print(f"trace created: {trace.id} (task: {trace.task[:50]}…)")
        await memory.reasoning.complete_trace(trace.id, success=True, outcome="Refund issued")

        print("\n== get_similar_traces ==")
        similar = await memory.reasoning.get_similar_traces(
            "Refund duplicate charge on Acme Cloud Compute", limit=3
        )
        print(f"retrieved {len(similar)} similar trace(s)")
        for t in similar:
            print(f"  - {t.task[:60]} (success={t.success})")

        print("\n== graph shape (AgentStep / ToolCall / TOUCHED) ==")
        rows = await memory.query.cypher(
            "MATCH (n) RETURN labels(n) AS labels, count(*) AS n ORDER BY n DESC"
        )
        for row in rows:
            print(f"  {row['labels']}: {row['n']}")
        touched = await memory.query.cypher(
            "MATCH ()-[r]->() WHERE type(r) IN ['TOUCHED', 'MENTIONS'] "
            "RETURN type(r) AS type, count(*) AS n"
        )
        for row in touched:
            print(f"  rel {row['type']}: {row['n']}")


if __name__ == "__main__":
    asyncio.run(main())
