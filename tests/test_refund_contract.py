import math

import pytest

from lib import db
from scripts import seed_sqlite


@pytest.fixture
def connection(tmp_path, monkeypatch):
    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    with db.connect(seed_sqlite.DB_PATH) as connection:
        yield connection


def refund(connection, email="maya.chen@northwind.example", amount=49, **options):
    return db.issue_refund(
        connection,
        email,
        amount,
        "duplicate charge",
        incident_id="maya-duplicate-compute",
        authorized_email=email,
        authorized=True,
        **options,
    )


def test_refund_is_idempotent_and_keeps_the_confirmed_customer(connection):
    first = refund(connection)
    again = refund(connection)
    assert first["status"] == "issued"
    assert again["status"] == "already_issued"
    assert first["refund_id"] == again["refund_id"]
    assert refund(connection, email="dana.w@contoso.example")["status"] == "rejected_wrong_account"
    assert connection.execute("SELECT count(*) FROM refunds").fetchone()[0] == 1


@pytest.mark.parametrize("amount", [-49, 0, math.nan, math.inf])
def test_non_positive_or_non_finite_refunds_never_write(connection, amount):
    assert refund(connection, amount=amount)["status"] == "rejected_invalid_amount"
    assert connection.execute("SELECT count(*) FROM refunds").fetchone()[0] == 0


def test_a_pro_case_cannot_use_the_previous_enterprise_account(connection):
    result = db.issue_refund(
        connection,
        "dana.w@contoso.example",
        400,
        "ops Pro account",
        incident_id="ravi-spot-capacity",
        authorized=True,
        authorized_email="ravi.shah@northwind.example",
    )
    assert result["status"] == "rejected_wrong_account"
    result = db.issue_refund(
        connection,
        "ravi.shah@northwind.example",
        400,
        "spot capacity",
        incident_id="ravi-spot-capacity",
        authorized=True,
        authorized_email="ravi.shah@northwind.example",
    )
    assert result["status"] == "rejected_over_limit"
    assert result["no_approval_limit"] == 250
    assert connection.execute("SELECT count(*) FROM refunds").fetchone()[0] == 0


def test_unconfirmed_and_mismatched_requests_never_write(connection):
    assert (
        db.issue_refund(connection, "maya.chen@northwind.example", 49, "update")["status"]
        == "requires_confirmation"
    )
    assert refund(connection, amount=48)["status"] == "rejected_case_amount"
