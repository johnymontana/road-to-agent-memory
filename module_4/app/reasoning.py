"""Lesson-owned execution recording and bounded procedure retrieval."""

from __future__ import annotations

import json
from uuid import UUID

from neo4j_agent_memory.schema.models import EntityRef, TraceOutcome


async def reasoning_examples(memory, query, embedder, namespace):
    embedding = await embedder.embed(query)
    rows = await memory.query.cypher(
        """// workshop:reasoning
        MATCH (t:ReasoningTrace)
        WHERE t.session_id STARTS WITH $namespace AND t.task_embedding IS NOT NULL
        WITH t,vector.similarity.cosine(t.task_embedding,$embedding) AS score
        WHERE score >= 0.45
        RETURN t.id AS id,t.task AS task,t.success AS success,score
        ORDER BY score DESC LIMIT 3""",
        {"namespace": namespace + ":", "embedding": embedding},
    )
    examples = []
    evidence = []
    for row in rows:
        trace = await memory.reasoning.get_trace_with_steps(UUID(row["id"]))
        if trace is None:
            continue
        try:
            outcome = json.loads(trace.outcome or "{}")
        except (ValueError, TypeError):
            outcome = {"summary": trace.outcome}
        examples.append(
            {
                "id": str(trace.id),
                "task": trace.task,
                "success": trace.success,
                "outcome": outcome,
                "steps": [
                    {
                        "action": s.action,
                        "observation": s.observation,
                        "tools": [
                            {"name": t.tool_name, "arguments": t.arguments, "result": t.result}
                            for t in s.tool_calls
                        ],
                    }
                    for s in trace.steps
                ],
            }
        )
        evidence.append({"id": str(trace.id), "path": "reasoning_trace", "score": row["score"]})
    return json.dumps(examples, default=str) if examples else "", evidence


async def finish_execution(memory, trace, message, calls, reply, execution_ok, warnings, case):
    refs = []
    business_status = next(
        (
            call["output"]["status"]
            for call in reversed(calls)
            if call["name"] in ("issue_refund", "refund_policy_guard")
        ),
        "no_action",
    )
    recording_error = None
    try:
        if case:
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
        if message is not None:
            await memory.reasoning.link_trace_to_message(trace.id, str(message.id))
        for call in calls:
            output = call["output"]
            step = await memory.reasoning.add_step(
                trace.id,
                action=call["name"],
                observation=json.dumps(output, default=str),
                generate_embedding=False,
            )
            await memory.reasoning.record_tool_call(
                step.id,
                call["name"],
                arguments=call["input"],
                result={"value": output, "executed_sql": call.get("sql")},
                message_id=str(message.id) if message is not None else None,
                touched_entities=refs,
                duration_ms=round(call["duration_ms"]),
            )
    except Exception as error:
        recording_error = type(error).__name__
        raise
    finally:
        rejected = (
            business_status.startswith("rejected") or business_status == "requires_confirmation"
        )
        await memory.reasoning.complete_trace(
            trace.id,
            outcome=TraceOutcome(
                success=execution_ok and not rejected and recording_error is None,
                summary=json.dumps(
                    {
                        "reply": reply,
                        "execution_status": "succeeded" if execution_ok else "failed",
                        "business_status": business_status,
                        "warnings": warnings,
                    },
                    default=str,
                ),
                error_kind=recording_error
                or (
                    "execution_error"
                    if not execution_ok
                    else "policy_declined"
                    if rejected
                    else None
                ),
                related_entities=refs,
                metrics={
                    "execution_succeeded": float(execution_ok),
                    "policy_compliant": 1.0,
                    "tool_calls": float(len(calls)),
                },
            ),
        )
