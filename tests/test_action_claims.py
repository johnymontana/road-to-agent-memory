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
    tools = importlib.import_module(f"module_{number}.app.tools")
    assert "No new refund or escalation was performed" in tools.verified_reply(
        "Please help", claim, []
    )
