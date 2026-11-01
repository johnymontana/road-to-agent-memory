"""Business tools owned by this lesson, backed by shared SQLite queries.

Each tool collects its name, input, SQL, output and duration for the caller's
trace panel. Tool definitions are intentionally copied into every lesson.
"""

from __future__ import annotations

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
            "input": tool_input,
            "sql": sql,
            "output": output,
            "duration_ms": round((time.monotonic() - started) * 1000, 1),
        }
    )
    return output


async def lookup_account(ctx: RunContext[ToolDeps], customer_email: str) -> dict[str, Any]:
    """Look up a customer's account (plan, organization, refund limit) by email."""
    started = time.monotonic()
    with dbx.connect(ctx.deps.db_path) as conn:
        out = dbx.lookup_account(conn, customer_email)
    return _record(
        ctx,
        "lookup_account",
        {"customer_email": customer_email},
        dbx.LOOKUP_ACCOUNT_SQL,
        started,
        out or {"error": f"no account for {customer_email}"},
    )


async def search_product_catalog(ctx: RunContext[ToolDeps], query: str) -> dict[str, Any]:
    """Search the Acme Cloud product catalog by name, description, or category."""
    started = time.monotonic()
    with dbx.connect(ctx.deps.db_path) as conn:
        out = dbx.search_products(conn, query)
    return _record(
        ctx,
        "search_product_catalog",
        {"query": query},
        dbx.SEARCH_PRODUCTS_SQL,
        started,
        {"matches": out, "count": len(out)},
    )


async def fetch_policy(ctx: RunContext[ToolDeps], topic: str) -> dict[str, Any]:
    """Fetch an Acme Cloud policy by topic (refund, sla, api_key_rotation, data_export)."""
    started = time.monotonic()
    with dbx.connect(ctx.deps.db_path) as conn:
        out = dbx.fetch_policy(conn, topic)
    return _record(
        ctx,
        "fetch_policy",
        {"topic": topic},
        dbx.FETCH_POLICY_SQL,
        started,
        out or {"error": f"no policy for topic '{topic}'"},
    )


async def check_service_status(ctx: RunContext[ToolDeps], service: str) -> dict[str, Any]:
    """Check the current status of an Acme Cloud service (e.g. 'Compute', 'Billing API')."""
    started = time.monotonic()
    with dbx.connect(ctx.deps.db_path) as conn:
        out = dbx.service_status(conn, service)
    return _record(
        ctx,
        "check_service_status",
        {"service": service},
        dbx.SERVICE_STATUS_SQL,
        started,
        {"services": out},
    )


async def issue_refund(
    ctx: RunContext[ToolDeps], customer_email: str, amount: float, reason: str
) -> dict[str, Any]:
    """Issue a refund, validated against the plan's no-approval limit from policy."""
    started = time.monotonic()
    with dbx.connect(ctx.deps.db_path) as conn:
        out = dbx.issue_refund(conn, customer_email, amount, reason)
    return _record(
        ctx,
        "issue_refund",
        {"customer_email": customer_email, "amount": amount, "reason": reason},
        dbx.INSERT_REFUND_SQL,
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
