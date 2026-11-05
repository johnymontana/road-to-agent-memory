import importlib

import pytest


@pytest.mark.parametrize("number", range(1, 6))
@pytest.mark.parametrize(
    "claim",
    [
        "Your ticket has been escalated to engineering.",
        "I will escalate this.",
        "I'll escalate the ticket.",
        "A refund was processed.",
        "We processed your refund.",
        "You have been refunded.",
    ],
)
def test_action_confirmation_requires_a_receipt(number, claim):
    guardrails = importlib.import_module(f"module_{number}.app.guardrails")
    assert "No new refund or escalation was performed" in guardrails.verified_reply(
        "Please help", claim, []
    )


@pytest.mark.parametrize("number", range(1, 6))
def test_blocked_claim_keeps_the_looked_up_account_and_history(number):
    guardrails = importlib.import_module(f"module_{number}.app.guardrails")
    account = {
        "name": "Maya Chen",
        "email": "maya@example.test",
        "plan": "Pro",
        "refund_limit": 250.0,
        "refunds": [],
    }
    calls = [{"name": "lookup_account", "output": account}]
    reply = guardrails.verified_reply("History please", "Your last refund was processed.", calls)
    assert "Maya Chen (maya@example.test), Pro plan" in reply
    assert "Recorded SQL refund history: none" in reply
    assert "No new refund or escalation was performed" in reply


@pytest.mark.parametrize("number", range(1, 6))
def test_already_refunded_case_reports_its_receipt(number, tmp_path, monkeypatch):
    from lib import db
    from scripts import seed_sqlite

    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    guardrails = importlib.import_module(f"module_{number}.app.guardrails")
    tools = importlib.import_module(f"module_{number}.app.tools")
    email = "ravi.shah@northwind.example"
    with db.connect(seed_sqlite.DB_PATH) as conn:
        db.issue_refund(
            conn,
            email,
            49,
            "dup",
            incident_id="ravi-duplicate-compute",
            authorized_email=email,
            authorized=True,
        )
    deps = tools.ToolDeps(
        db_path=seed_sqlite.DB_PATH,
        account_email=email,
        incident_id="ravi-duplicate-compute",
        authorize_refund=True,
    )
    scope = guardrails.scope_turn(deps, None)
    assert "already refunded" in scope.instructions
    reply = guardrails.checked_reply("again", "Your refund was processed again.", deps, scope)
    assert reply.startswith("Billing case ravi-duplicate-compute was already refunded: refund #")
