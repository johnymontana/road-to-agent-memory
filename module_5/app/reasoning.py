"""Reasoning memory: record how each turn was handled, and recall similar ones.

- `similar_executions` runs before the model call. It finds past turns whose
  task resembles this message and returns their steps and outcomes as examples.
- `record_execution` runs after the turn. It saves each tool call as a step of
  the turn's (:ReasoningTrace), then completes the trace with its outcome.

Why not the library's helpers?
- `reasoning.get_similar_traces()` searches the global vector index top-k and
  cannot filter by namespace. The ablation compares two branches against one
  fixed corpus namespace, so retrieval must be namespace-exact. It also needs
  failed (policy-declined) traces, which are often the most useful examples.
- `integrations.pydantic_ai.record_agent_trace()` needs a completed
  `AgentRunResult`. This app also records failed runs, which have no result, and
  server-side guard decisions that are not model tool calls. It also stores the
  executed SQL with each step.

What a trace holds: the tools that ran, with their inputs, outputs and SQL, plus
the outcome. It does not hold the model's hidden reasoning.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from neo4j_agent_memory.schema.models import EntityRef, TraceOutcome

from lib.response import business_status

EXAMPLE_LIMIT = 3
SIMILARITY_THRESHOLD = 0.45  # Task wording varies more than facts do; match loosely.


async def similar_executions(memory, query, embedder, namespace) -> tuple[str, list[dict]]:
    """Past executions similar to `query`, as JSON examples plus evidence records.

    Only completed traces count. This turn's own trace is already open (step 0 in
    agent.py) and its task is this exact message, so it would otherwise match itself.
    """
    embedding = await embedder.embed(query)
    rows = await memory.query.cypher(
        """// workshop:reasoning
        MATCH (t:ReasoningTrace)
        WHERE t.session_id STARTS WITH $namespace AND t.task_embedding IS NOT NULL
          AND t.completed_at IS NOT NULL
        WITH t,vector.similarity.cosine(t.task_embedding,$embedding) AS score
        WHERE score >= $threshold
        RETURN t.id AS id,t.task AS task,t.success AS success,score
        ORDER BY score DESC LIMIT $limit""",
        {
            "namespace": namespace + ":",
            "embedding": embedding,
            "threshold": SIMILARITY_THRESHOLD,
            "limit": EXAMPLE_LIMIT,
        },
    )
    examples = []
    evidence = []
    for row in rows:
        trace = await memory.reasoning.get_trace_with_steps(UUID(row["id"]))
        if trace is None:
            continue
        examples.append(as_example(trace))
        evidence.append({"id": str(trace.id), "path": "reasoning_trace", "score": row["score"]})
    return (json.dumps(examples, default=str) if examples else ""), evidence


def as_example(trace) -> dict[str, Any]:
    """A trace in the compact shape the model reads: task, outcome and steps."""
    try:
        outcome = json.loads(trace.outcome or "{}")
    except (ValueError, TypeError):
        outcome = {"summary": trace.outcome}
    return {
        "id": str(trace.id),
        "task": trace.task,
        "success": trace.success,
        "outcome": outcome,
        "steps": [
            {
                "action": step.action,
                "observation": step.observation,
                "tools": [
                    {"name": t.tool_name, "arguments": t.arguments, "result": t.result}
                    for t in step.tool_calls
                ],
            }
            for step in trace.steps
        ],
    }


async def record_execution(
    memory,
    trace,
    *,
    message,
    tool_calls: list[dict],
    reply: str,
    execution_ok: bool,
    warnings: list[dict],
    case: dict | None,
) -> None:
    """Save each tool call as a step, then complete the trace (also on failure)."""
    status = business_status(tool_calls)
    recording_error = None
    refs: list[EntityRef] = []
    try:
        if case:
            refs = await case_entities(memory, case)
        if message is not None:
            await memory.reasoning.link_trace_to_message(trace.id, str(message.id))
        for call in tool_calls:
            step = await memory.reasoning.add_step(
                trace.id,
                action=call["name"],
                observation=json.dumps(call["output"], default=str),
                generate_embedding=False,
            )
            await memory.reasoning.record_tool_call(
                step.id,
                call["name"],
                arguments=call["input"],
                result={"value": call["output"], "executed_sql": call.get("sql")},
                message_id=str(message.id) if message is not None else None,
                touched_entities=refs,
                duration_ms=round(call["duration_ms"]),
            )
    except Exception as error:
        recording_error = type(error).__name__
        raise
    finally:
        declined = status.startswith("rejected") or status == "requires_confirmation"
        if recording_error:
            error_kind = recording_error
        elif not execution_ok:
            error_kind = "execution_error"
        elif declined:
            error_kind = "policy_declined"
        else:
            error_kind = None
        await memory.reasoning.complete_trace(
            trace.id,
            outcome=TraceOutcome(
                success=error_kind is None,
                summary=json.dumps(
                    {
                        "reply": reply,
                        "execution_status": "succeeded" if execution_ok else "failed",
                        "business_status": status,
                        "warnings": warnings,
                    },
                    default=str,
                ),
                error_kind=error_kind,
                related_entities=refs,
                metrics={
                    "execution_succeeded": float(execution_ok),
                    "tool_calls": float(len(tool_calls)),
                },
            ),
        )


async def case_entities(memory, case: dict) -> list[EntityRef]:
    """The customer and plan of the selected billing case, as entity references."""
    refs = []
    for name, etype, subtype, description in (
        (case["customer"], "PERSON", "CUSTOMER", f"{case['customer']} ({case['email']})"),
        (case["plan"], "OBJECT", "PLAN", f"No-approval limit ${case['refund_limit']:.2f}"),
    ):
        entity, _ = await memory.long_term.add_entity(
            name,
            etype,
            subtype=subtype,
            description=description,
            resolve=False,
            deduplicate=False,
            enrich=False,
            generate_embedding=False,
        )
        refs.append(EntityRef(id=str(entity.id)))
    return refs
