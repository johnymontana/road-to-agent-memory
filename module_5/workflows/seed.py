#!/usr/bin/env python3
"""make nams-seed — populate the attendee's NAMS workspace with the canonical
reasoning memory (module 5). Pre-seeded snapshot approach (decision D2).

Writes in realistic agent-loop order: entities → conversation → messages →
reasoning traces (steps + tool calls with JSON-string payloads). Entity upserts
may merge; conversations and traces are newly seeded on each run.
Live NAMS verification is tracked separately in docs/verification-log.md.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

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


async def main() -> None:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    if not s.nams_api_key:
        print("NAMS_API_KEY not set — run make nams-check first.")
        sys.exit(1)
    headers = {"Authorization": f"Bearer {s.nams_api_key}"}
    async with httpx.AsyncClient(base_url=s.nams_base_url, headers=headers, timeout=30.0) as http:
        print("Seeding entities…")
        entity_ids: dict[str, str] = {}
        for ent in ENTITIES:
            resp = await http.post("/v1/entities", json=ent)
            resp.raise_for_status()
            body = resp.json()
            entity_ids[ent["name"]] = body.get("id") or body.get("merged_into")

        print("Creating conversation + messages…")
        resp = await http.post("/v1/conversations", json={"userId": "maya.chen"})
        resp.raise_for_status()
        conv_id = resp.json()["id"]
        resp = await http.post(
            f"/v1/conversations/{conv_id}/messages/bulk", json={"messages": MESSAGES}
        )
        resp.raise_for_status()

        print("Writing reasoning traces (steps + tool calls, agent-loop order)…")
        for trace in TRACES:
            resp = await http.post(
                "/v1/reasoning/traces",
                json={
                    "conversationId": conv_id,
                    "task": trace["task"],
                },
            )
            resp.raise_for_status()
            trace_id = resp.json()["id"]
            for step in trace["steps"]:
                resp = await http.post(
                    "/v1/reasoning/steps",
                    json={
                        "traceId": trace_id,
                        "conversationId": conv_id,
                        "reasoning": step["reasoning"],
                        "actionTaken": step["actionTaken"],
                        "result": step["result"],
                    },
                )
                resp.raise_for_status()
                step_id = resp.json()["id"]
                tool = step["tool"]
                resp = await http.post(
                    "/v1/reasoning/tool-calls",
                    json={
                        "stepId": step_id,
                        "toolName": tool["toolName"],
                        # NAMS expects input/output as JSON-encoded STRINGS
                        "input": json.dumps(tool["input"]),
                        "output": json.dumps(tool["output"]),
                        "status": "success",
                        "touchedEntityIds": [entity_ids["Maya Chen"]],
                    },
                )
                resp.raise_for_status()

        print(
            f"Done. Conversation {conv_id}, {len(TRACES)} traces, "
            f"{len(ENTITIES)} entities. Next: make nams-distill"
        )


if __name__ == "__main__":
    asyncio.run(main())
