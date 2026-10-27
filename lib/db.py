"""SQLite access for the Acme Cloud system of record (stdlib sqlite3 only).

Every query is parameterized — the tools are agent-facing, so injection safety
and typed results are part of the workshop's teaching surface.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def rows_as_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]


# ── Query helpers backing the agent tools ─────────────────────────────────────

LOOKUP_ACCOUNT_SQL = (
    "SELECT c.id, c.name, c.email, c.signup_date, c.preferred_contact, "
    "o.name AS organization, p.name AS plan, p.tier AS plan_tier, "
    "p.monthly_price, p.refund_limit "
    "FROM customers c "
    "LEFT JOIN organizations o ON c.organization_id = o.id "
    "LEFT JOIN plans p ON c.plan_id = p.id "
    "WHERE c.email = ?"
)

SEARCH_PRODUCTS_SQL = (
    "SELECT p.id, p.name, p.sku, p.description, p.category, "
    "GROUP_CONCAT(f.name, '; ') AS features "
    "FROM products p LEFT JOIN features f ON f.product_id = p.id "
    "WHERE p.name LIKE ? OR p.description LIKE ? OR p.category LIKE ? "
    "GROUP BY p.id"
)

FETCH_POLICY_SQL = "SELECT topic, title, body, updated_at FROM policies WHERE topic = ?"

SERVICE_STATUS_SQL = (
    "SELECT service, status, detail, updated_at FROM service_status WHERE service LIKE ?"
)

INSERT_REFUND_SQL = (
    "INSERT INTO refunds (customer_id, amount, reason, status, created_at) "
    "VALUES (?, ?, ?, ?, datetime('now'))"
)

CUSTOMER_PLAN_SQL = (
    "SELECT c.id, c.name, p.name AS plan, p.refund_limit FROM customers c "
    "JOIN plans p ON c.plan_id = p.id WHERE c.email = ?"
)


def lookup_account(db: sqlite3.Connection, email: str) -> dict[str, Any] | None:
    row = db.execute(LOOKUP_ACCOUNT_SQL, (email,)).fetchone()
    return dict(row) if row else None


def search_products(db: sqlite3.Connection, query: str) -> list[dict[str, Any]]:
    like = f"%{query}%"
    return rows_as_dicts(db.execute(SEARCH_PRODUCTS_SQL, (like, like, like)).fetchall())


def fetch_policy(db: sqlite3.Connection, topic: str) -> dict[str, Any] | None:
    row = db.execute(FETCH_POLICY_SQL, (topic,)).fetchone()
    return dict(row) if row else None


def service_status(db: sqlite3.Connection, service: str) -> list[dict[str, Any]]:
    return rows_as_dicts(db.execute(SERVICE_STATUS_SQL, (f"%{service}%",)).fetchall())


def issue_refund(
    db: sqlite3.Connection, email: str, amount: float, reason: str
) -> dict[str, Any]:
    """Validate against the plan's no-approval refund limit, then write.

    Over-limit requests are REJECTED (not silently approved) — this is the
    module 4 failed-trace beat and the policy grounding for the module 5 skill.
    """
    row = db.execute(CUSTOMER_PLAN_SQL, (email,)).fetchone()
    if row is None:
        return {"status": "rejected", "reason": f"no account for {email}"}
    customer = dict(row)
    limit = customer["refund_limit"]
    if amount > limit:
        return {
            "status": "rejected_over_limit",
            "amount": amount,
            "plan": customer["plan"],
            "no_approval_limit": limit,
            "reason": (
                f"${amount:.2f} exceeds the {customer['plan']} plan's "
                f"no-approval refund limit of ${limit:.2f}; escalate for manager approval."
            ),
        }
    cur = db.execute(INSERT_REFUND_SQL, (customer["id"], amount, reason, "issued"))
    db.commit()
    return {
        "status": "issued",
        "refund_id": cur.lastrowid,
        "amount": amount,
        "customer": customer["name"],
        "plan": customer["plan"],
    }
