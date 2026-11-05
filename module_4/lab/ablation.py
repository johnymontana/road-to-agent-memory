"""Ablation corpus for `make s4-refund-repeat`: one fixed, rejected refund trace.

Both branches (retrieval off / on) read this same corpus, so the only difference
between them is whether the agent retrieves past executions.
"""

import json

from neo4j_agent_memory.schema.models import TraceOutcome

from lib import db as dbx

from ..app.memory import open_memory


async def seed_corpus(settings, namespace):
    with dbx.connect(settings.db_path) as db:
        result = dbx.issue_refund(
            db,
            "ravi.shah@northwind.example",
            400,
            "Fixed Pro policy example",
            incident_id="ravi-spot-capacity",
            authorized_email="ravi.shah@northwind.example",
            authorized=True,
        )
    if result["status"] != "rejected_over_limit":
        raise ValueError(
            "The fixed Pro example must exceed the current policy limit; "
            "restore the workshop fixture"
        )
    async with open_memory(settings) as memory:
        trace = await memory.reasoning.start_trace(
            namespace + ":example",
            "How to handle a Pro plan $400 unused spot capacity refund request",
        )
        step = await memory.reasoning.add_step(
            trace.id,
            action="refund_policy_guard",
            observation=json.dumps(result),
            generate_embedding=False,
        )
        await memory.reasoning.record_tool_call(
            step.id,
            "refund_policy_guard",
            arguments={"incident_id": "ravi-spot-capacity"},
            result=result,
        )
        await memory.reasoning.complete_trace(
            trace.id,
            outcome=TraceOutcome(
                success=False,
                summary=json.dumps(
                    {
                        "reply": result["reason"],
                        "business_status": result["status"],
                        "execution_status": "succeeded",
                    }
                ),
                error_kind="policy_declined",
            ),
        )
        return str(trace.id)
