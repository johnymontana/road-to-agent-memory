"""Seed data tests — the Acme Cloud dataset must make every tool meaningful."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import db as dbx  # noqa: E402


def seeded_db(tmp_path: Path) -> sqlite3.Connection:
    """Re-seed deterministically, then return a connection."""
    import importlib

    seed = importlib.import_module("scripts.seed_sqlite")
    importlib.reload(seed)
    original = seed.DB_PATH
    seed.DB_PATH = tmp_path / "acme_cloud.db"
    try:
        seed.main()
        return dbx.connect(seed.DB_PATH)
    finally:
        seed.DB_PATH = original


def test_setup_keeps_existing_workshop_state(tmp_path, monkeypatch):
    from scripts import seed_sqlite

    path = tmp_path / "acme_cloud.db"
    monkeypatch.setattr(seed_sqlite, "DB_PATH", path)
    seed_sqlite.main(if_missing=True)
    with sqlite3.connect(path) as db:
        db.execute("UPDATE plans SET refund_limit=123 WHERE name='Pro'")
    seed_sqlite.main(if_missing=True)
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT refund_limit FROM plans WHERE name='Pro'").fetchone() == (123,)
    seed_sqlite.main()
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT refund_limit FROM plans WHERE name='Pro'").fetchone() == (250,)


def test_all_tables_seeded(tmp_path):
    conn = seeded_db(tmp_path)
    for table, minimum in {
        "customers": 3,
        "organizations": 2,
        "products": 4,
        "features": 5,
        "plans": 3,
        "subscriptions": 5,
        "policies": 4,
        "service_status": 5,
    }.items():
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert count >= minimum, f"{table}: expected ≥{minimum}, got {count}"
    conn.close()


def test_every_tool_returns_data(tmp_path):
    conn = seeded_db(tmp_path)
    assert dbx.lookup_account(conn, "maya.chen@northwind.example")["plan"] == "Pro"
    assert len(dbx.search_products(conn, "compute")) >= 1
    assert dbx.fetch_policy(conn, "refund")["title"] == "Refund Policy"
    assert any(
        s["service"] == "Acme Cloud Functions" for s in dbx.service_status(conn, "Functions")
    )
    conn.close()


def test_issue_refund_limit_enforcement(tmp_path):
    conn = seeded_db(tmp_path)
    # Within the Pro no-approval limit ($250): issued
    ok = dbx.issue_refund(
        conn,
        "maya.chen@northwind.example",
        49.0,
        "duplicate charge",
        incident_id="maya-duplicate-compute",
        authorized_email="maya.chen@northwind.example",
        authorized=True,
    )
    assert ok["status"] == "issued"
    # Over the limit: rejected — the module 4 failed-trace beat
    over = dbx.issue_refund(
        conn,
        "maya.chen@northwind.example",
        400.0,
        "spot capacity",
        incident_id="maya-spot-capacity",
        authorized_email="maya.chen@northwind.example",
        authorized=True,
    )
    assert over["status"] == "rejected_over_limit"
    assert over["no_approval_limit"] == 250.0
    # Enterprise ($500 limit): the s4-refund-repeat ticket succeeds
    ent = dbx.issue_refund(
        conn,
        "dana.w@contoso.example",
        129.0,
        "double-billed",
        incident_id="dana-duplicate-storage",
        authorized_email="dana.w@contoso.example",
        authorized=True,
    )
    assert ent["status"] == "issued"
    conn.close()


def test_external_status_is_unknown_even_with_legacy_seed_row(tmp_path):
    conn = seeded_db(tmp_path)
    assert dbx.service_status(conn, "Stripe") == []
    conn.close()
