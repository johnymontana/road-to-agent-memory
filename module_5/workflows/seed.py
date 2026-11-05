#!/usr/bin/env python3
"""make nams-seed — populate the attendee's NAMS workspace with the canonical
reasoning memory (module 5). Pre-seeded snapshot approach (decision D2).

Writes in realistic agent-loop order: entities → conversation → messages →
reasoning traces (steps + tool calls with JSON-string payloads) → trace completion.
Each run gets a fresh user scope for its entities and conversation.
The seeded conversation ID is saved for `make nams-distill`, which distills from
exactly this history.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from uuid import uuid4

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

POLICY_NAME = "Acme Cloud Refund Policy"

ENTITIES = [
    {
        "name": "Maya Chen",
        "type": "person",
        "description": "Pro plan customer at Northwind Robotics.",
    },
    {
        "name": "Northwind Robotics",
        "type": "organization",
        "description": "Robotics company, Acme Cloud customer.",
    },
    {
        "name": "Acme Cloud Compute",
        "type": "custom",
        "description": "Autoscaling container compute product.",
    },
    {
        "name": "Pro",
        "type": "custom",
        "description": "Mid-tier plan; no-approval refund limit $250.",
    },
    {
        "name": POLICY_NAME,
        "type": "custom",
        "description": "Duplicate charges qualify for a refund; Pro's no-approval limit is $250.",
    },
]

MESSAGES = [
    {
        "role": "user",
        "content": "Hi, Maya Chen (maya.chen@northwind.example), Pro plan. "
        "I was double-charged $49 for Acme Cloud Compute — please refund it.",
    },
    {
        "role": "assistant",
        "content": "I've confirmed your Pro plan and the refund policy "
        "covers duplicate charges. Issuing a $49 refund now.",
    },
    {"role": "user", "content": "Thanks! While you're here — is the Billing API stable?"},
    {"role": "assistant", "content": "Billing API is operational; webhook delivery is nominal."},
]

# The canonical refund procedure, observed twice (so distillation sees a pattern).
TRACES = [
    {
        "task": "Refund duplicate $49 Acme Cloud Compute charge for Maya Chen",
        "outcome": "Refund issued: duplicate $49 charge, within the Pro no-approval limit.",
        "steps": [
            {
                "reasoning": "Identify the customer and plan before touching money.",
                "actionTaken": "lookup_account",
                "tool": {
                    "toolName": "lookup_account",
                    "input": {"customer_email": "maya.chen@northwind.example"},
                    "output": {"plan": "Pro", "refund_limit": 250.0},
                },
                "result": "Pro plan, no-approval limit $250",
            },
            {
                "reasoning": "Check the refund policy before issuing.",
                "actionTaken": "fetch_policy",
                "tool": {
                    "toolName": "fetch_policy",
                    "input": {"topic": "refund"},
                    "output": {"title": "Refund Policy"},
                },
                "result": "Duplicate charges always refundable; ≤$250 on Pro needs no approval",
            },
            {
                "reasoning": "Amount is within the limit and it is a duplicate charge — issue it.",
                "actionTaken": "issue_refund",
                "tool": {
                    "toolName": "issue_refund",
                    "input": {
                        "customer_email": "maya.chen@northwind.example",
                        "amount": 49.0,
                        "reason": "duplicate charge",
                    },
                    "output": {"status": "issued"},
                },
                "result": "Refund issued",
            },
        ],
    },
    {
        "task": "Refund duplicate $49 Acme Cloud Compute charge (repeat, one week later)",
        "outcome": "Refund issued: same duplicate-charge procedure as last week.",
        "steps": [
            {
                "reasoning": "Same shape as last week: verify account first.",
                "actionTaken": "lookup_account",
                "tool": {
                    "toolName": "lookup_account",
                    "input": {"customer_email": "maya.chen@northwind.example"},
                    "output": {"plan": "Pro", "refund_limit": 250.0},
                },
                "result": "Pro plan confirmed",
            },
            {
                "reasoning": "Policy check: duplicate charges are always refundable.",
                "actionTaken": "fetch_policy",
                "tool": {
                    "toolName": "fetch_policy",
                    "input": {"topic": "refund"},
                    "output": {"title": "Refund Policy"},
                },
                "result": "Policy confirmed",
            },
            {
                "reasoning": "Within limit — issue.",
                "actionTaken": "issue_refund",
                "tool": {
                    "toolName": "issue_refund",
                    "input": {
                        "customer_email": "maya.chen@northwind.example",
                        "amount": 49.0,
                        "reason": "duplicate charge",
                    },
                    "output": {"status": "issued"},
                },
                "result": "Refund issued",
            },
        ],
    },
]


def schema_rejection(entity: dict, response: httpx.Response) -> str:
    """Explain an HTTP 422: the workspace's active ontology does not accept a plain seed entity."""
    try:
        detail = response.json()
    except ValueError:
        detail = {}
    ontology = (detail.get("active_ontology") or {}).get("id", "custom")
    reason = detail.get("message") or response.text[:200]
    return (
        f"NAMS rejected the seed entity {entity['name']!r} ({entity['type']}): {reason}\n"
        f"This workspace's active ontology ({ontology}) requires more than the workshop seed "
        "provides. Point NAMS_API_KEY at a workshop workspace without a custom ontology "
        "(make nams-check reports it), then run make nams-seed again.\n"
        "Fallback: make s5-fresh-agent WITH_SKILL=fallback"
    )


async def main() -> None:
    from lib.settings import get_settings
    from module_5.workflows.nams import call, client, seed_state_path, write_json

    settings = get_settings()
    user_id = f"workshop-maya-{uuid4()}"
    async with client(settings) as http:
        print("Seeding entities…")
        entity_ids: dict[str, str] = {}
        for entity in ENTITIES:
            try:
                body = await call(http, "POST", "/v1/entities", {**entity, "userId": user_id})
            except httpx.HTTPStatusError as error:
                if error.response.status_code != 422:
                    raise
                sys.exit(schema_rejection(entity, error.response))
            # 201 creates it; 200 means it resolved onto an existing entity.
            entity_ids[entity["name"]] = body.get("id") or body.get("merged_into")

        print("Creating conversation + messages…")
        conversation = await call(http, "POST", "/v1/conversations", {"userId": user_id})
        conv_id = conversation["id"]
        added = await call(
            http, "POST", f"/v1/conversations/{conv_id}/messages/bulk", {"messages": MESSAGES}
        )
        first_message_id = added["messages"][0]["id"]

        print("Writing reasoning traces (steps + tool calls, agent-loop order)…")
        trace_ids = []
        for trace in TRACES:
            started = await call(
                http,
                "POST",
                "/v1/reasoning/traces",
                {
                    "conversationId": conv_id,
                    "task": trace["task"],
                    "triggeredByMessageId": first_message_id,
                },
            )
            trace_id = started["id"]
            for step in trace["steps"]:
                recorded = await call(
                    http,
                    "POST",
                    "/v1/reasoning/steps",
                    {
                        "traceId": trace_id,
                        "reasoning": step["reasoning"],
                        "actionTaken": step["actionTaken"],
                        "result": step["result"],
                    },
                )
                tool = step["tool"]
                touched = POLICY_NAME if tool["toolName"] == "fetch_policy" else "Maya Chen"
                await call(
                    http,
                    "POST",
                    "/v1/reasoning/tool-calls",
                    {
                        "stepId": recorded["id"],
                        "toolName": tool["toolName"],
                        # NAMS expects input/output as JSON-encoded STRINGS
                        "input": json.dumps(tool["input"]),
                        "output": json.dumps(tool["output"]),
                        "status": "success",
                        "touchedEntityIds": [entity_ids[touched]],
                    },
                )
            # A completed, successful trace is what distillation learns a procedure from.
            await call(
                http,
                "POST",
                f"/v1/reasoning/traces/{trace_id}/complete",
                {
                    "outcome": trace["outcome"],
                    "success": True,
                    "relatedEntityIds": [entity_ids["Maya Chen"], entity_ids[POLICY_NAME]],
                },
            )
            trace_ids.append(trace_id)

    write_json(
        seed_state_path(settings),
        {
            "conversationId": conv_id,
            "traceIds": trace_ids,
            "userId": user_id,
            "policyEntityId": entity_ids[POLICY_NAME],
        },
    )
    print(
        f"Done. Conversation {conv_id}, {len(TRACES)} completed traces, "
        f"{len(ENTITIES)} entities. Next: make nams-distill"
    )


if __name__ == "__main__":
    asyncio.run(main())
