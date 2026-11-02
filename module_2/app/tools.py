"""Business tools owned by this lesson, backed by shared SQLite queries.

Each tool collects its name, input, SQL, output and duration for the caller's
trace panel. Tool definitions are intentionally copied into every lesson.
"""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic_ai import RunContext

from lib import db as dbx


@dataclass
class ToolDeps:
    db_path: Path
    collector: list[dict[str, Any]] = field(default_factory=list)
    account_email: str | None = None
    incident_id: str | None = None
    authorize_refund: bool = False
    session_id: str = ""
    namespace: str = "workshop"
    current_message_id: str | None = None
    embedder: Any = None


def _receipt_value(value):
    """Keep rejected nonfinite attempts inspectable in standards-compliant JSON."""
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, dict):
        return {k: _receipt_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_receipt_value(v) for v in value]
    return value


def _record(
    ctx: RunContext[ToolDeps],
    name: str,
    tool_input: dict,
    sql: str | None,
    started: float,
    output: Any,
) -> Any:
    ctx.deps.collector.append(
        {
            "name": name,
            "input": _receipt_value(tool_input),
            "sql": sql,
            "output": _receipt_value(output),
            "duration_ms": round((time.monotonic() - started) * 1000, 1),
        }
    )
    return output


async def lookup_account(ctx: RunContext[ToolDeps], customer_email: str) -> dict[str, Any]:
    """Look up a customer's account (plan, organization, refund limit) by email."""
    started = time.monotonic()
    statements: list[str] = []
    with dbx.connect(ctx.deps.db_path, audit=statements) as conn:
        out = dbx.lookup_account(conn, customer_email)
    return _record(
        ctx,
        "lookup_account",
        {"customer_email": customer_email},
        "\n".join(statements),
        started,
        out or {"error": f"no account for {customer_email}"},
    )


async def search_product_catalog(ctx: RunContext[ToolDeps], query: str) -> dict[str, Any]:
    """Search the Acme Cloud product catalog by name, description, or category."""
    started = time.monotonic()
    statements: list[str] = []
    with dbx.connect(ctx.deps.db_path, audit=statements) as conn:
        out = dbx.search_products(conn, query)
    return _record(
        ctx,
        "search_product_catalog",
        {"query": query},
        "\n".join(statements),
        started,
        {"matches": out, "count": len(out)},
    )


async def fetch_policy(ctx: RunContext[ToolDeps], topic: str) -> dict[str, Any]:
    """Fetch an Acme Cloud policy by topic (refund, sla, api_key_rotation, data_export)."""
    started = time.monotonic()
    statements: list[str] = []
    with dbx.connect(ctx.deps.db_path, audit=statements) as conn:
        out = dbx.fetch_policy(conn, topic)
    return _record(
        ctx,
        "fetch_policy",
        {"topic": topic},
        "\n".join(statements),
        started,
        out or {"error": f"no policy for topic '{topic}'"},
    )


async def check_service_status(ctx: RunContext[ToolDeps], service: str) -> dict[str, Any]:
    """Read an Acme Cloud status snapshot with its observation timestamp."""
    started = time.monotonic()
    statements: list[str] = []
    with dbx.connect(ctx.deps.db_path, audit=statements) as conn:
        out = dbx.service_status(conn, service)
    return _record(
        ctx,
        "check_service_status",
        {"service": service},
        "\n".join(statements),
        started,
        {
            "services": out,
            "status": "known" if out else "unknown",
            "source": "sqlite:service_status",
            "notice": None
            if out
            else "No status source for this service; do not infer health from memory or Wikipedia.",
        },
    )


async def issue_refund(
    ctx: RunContext[ToolDeps], customer_email: str, amount: float, reason: str
) -> dict[str, Any]:
    """Issue a refund, validated against the plan's no-approval limit from policy."""
    started = time.monotonic()
    statements: list[str] = []
    with dbx.connect(ctx.deps.db_path, audit=statements) as conn:
        out = dbx.issue_refund(
            conn,
            customer_email,
            amount,
            reason,
            incident_id=ctx.deps.incident_id,
            authorized_email=ctx.deps.account_email,
            authorized=ctx.deps.authorize_refund,
        )
    return _record(
        ctx,
        "issue_refund",
        {"customer_email": customer_email, "amount": amount, "reason": reason},
        "\n".join(statements),
        started,
        out,
    )


SQLITE_TOOLS = [
    lookup_account,
    search_product_catalog,
    fetch_policy,
    check_service_status,
    issue_refund,
]


def verified_reply(message: str, reply: str, calls: list[dict]) -> str:
    """Business receipts override unsupported action claims in model prose."""
    refunds = [c["output"] for c in calls if c["name"] in ("issue_refund", "refund_policy_guard")]
    if refunds:
        result = refunds[-1]
        if result["status"] in ("issued", "already_issued"):
            verb = "Issued" if result["status"] == "issued" else "Previously issued"
            return (
                f"{verb} refund #{result['refund_id']}: ${result['amount']:.2f} "
                f"for {result['customer']} ({result['customer_email']}, {result['plan']}). "
                f"Incident: {result['incident_id']}. This incident cannot be refunded twice."
            )
        return "No refund was issued. " + result["reason"]
    statuses = [c["output"] for c in calls if c["name"] == "check_service_status"]
    if statuses and statuses[-1].get("status") == "known":
        rows = statuses[-1]["services"]
        return "Workshop snapshot (not live monitoring): " + "; ".join(
            f"{row['service']}: {row['status']} as of {row['updated_at']} (SQLite service_status)"
            for row in rows
        )
    if statuses and statuses[-1].get("status") == "unknown":
        return (
            "Current service status is unknown: this workshop has no verified "
            "status source for that service."
        )
    lower = message.lower()
    status_question = any(
        p in lower
        for p in ("status", "outage", "operational", "having issues", "showing any issues")
    )
    if status_question and not statuses:
        return (
            "No current service status was verified in this turn. Please name "
            "an Acme Cloud service so I can check it."
        )
    escalation = "escalat" in lower or "escalat" in reply.lower()
    refund_claim = re.search(
        r"\brefunded\b|\brefund\b.{0,60}\b(issued|processed|sent|completed|approved)\b"
        r"|\b(issue[ds]?|process(?:ed)?|sent|completed)\b.{0,60}\brefund\b",
        reply,
        re.I,
    )
    if escalation or refund_claim:
        policies = [
            c["output"].get("body", "")
            for c in calls
            if c["name"] == "fetch_policy" and isinstance(c["output"], dict)
        ]
        history = [
            refund
            for c in calls
            if c["name"] == "lookup_account" and isinstance(c["output"], dict)
            for refund in c["output"].get("refunds", [])
        ]
        detail = ""
        if policies:
            detail = "Current SQL policy: " + policies[-1] + " "
        if history:
            detail += (
                "Recorded SQL refund history: "
                + ", ".join(
                    f"#{r['refund_id']} ${r['amount']:.2f} ({r['status']})" for r in history
                )
                + ". "
            )
        return detail + (
            "No new refund or escalation was performed in this turn. "
            "Confirm a billing case for a refund; ask a manager for approval above the plan limit."
        )
    return reply


def validate_selected_case(deps):
    if not deps.authorize_refund or not deps.incident_id:
        return
    statements = []
    start = time.monotonic()
    with dbx.connect(deps.db_path, audit=statements) as db:
        case = dbx.case_details(db, deps.incident_id)
        if not case or case["amount"] <= case["refund_limit"]:
            return
        result = dbx.issue_refund(
            db,
            case["email"],
            case["amount"],
            "Confirmed case policy check",
            incident_id=deps.incident_id,
            authorized_email=deps.account_email,
            authorized=True,
        )
    deps.collector.append(
        {
            "name": "refund_policy_guard",
            "origin": "server_validation",
            "input": {"incident_id": deps.incident_id},
            "output": result,
            "sql": "\n".join(statements),
            "duration_ms": round((time.monotonic() - start) * 1000, 1),
        }
    )
