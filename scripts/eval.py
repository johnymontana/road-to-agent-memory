#!/usr/bin/env python3
"""make eval — the continuity eval thread. Asks the fixed question set and
prints the scorecard showing which module unlocks each answer."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Prime the eval session with a real support exchange so short-term memory has
# actual content to recall (the questions then test the layers, not an empty chat).
PRIME_MESSAGE = (
    "Hi, I'm Maya Chen from Northwind Robotics (maya.chen@northwind.example), on the "
    "Pro plan. I was double-charged $49 for Acme Cloud Compute, and Acme Cloud "
    "Functions looked degraded this morning."
)
# The continuity thread (WORKSHOP_OUTLINE.md, The Arc). expected_from_module is the
# first module whose memory layer makes the question answerable.
EVAL_QUESTIONS = [
    {
        "id": "q1",
        "question": "Do you remember the customer from Northwind Robotics? What's their name and email?",
        "expected_from_module": 2,  # cross-session conversation recall
        "signals": ["maya"],
    },
    {
        "id": "q2",
        "question": "What did we discuss earlier in this conversation?",
        "expected_from_module": 2,
        "signals": ["charge", "compute", "functions"],  # short-term memory: conversation history
    },
    {
        "id": "q3",
        "question": "I'm the Northwind Robotics customer on the Pro plan — what else do you know about my account, like how long I've been a customer?",
        "expected_from_module": 3,
        # signup date exists ONLY on the hydrated long-term entity — generic
        # policy text (tools) and conversation recall cannot produce it.
        "signals": ["2025", "march", "signup"],
    },
    {
        "id": "q4",
        "question": "Last week a customer asked you for a large refund on a Pro plan that you couldn't approve — what exactly did you tell them?",
        "expected_from_module": 4,
        # "spot capacity" and the rejection wording appear only in the recorded
        # failed interaction — not in this question, the policy text, or the
        # agent's restatement of the question.
        "signals": ["spot", "rejected", "couldn't", "cannot issue", "couldn't issue"],
    },
]


async def run_eval(chat) -> dict:
    results = []
    # Session A: primed with a real exchange — q2 tests short-term recall of it.
    session_a = f"eval-a-{chat.module}"
    await chat.chat(PRIME_MESSAGE, session_id=session_a)
    # Session B is fresh. Bolt can retrieve cross-session relevant messages;
    # these keyword checks illustrate recall, not causal isolation of layers.
    session_b = f"eval-b-{chat.module}"
    for q in EVAL_QUESTIONS:
        session = session_a if q["id"] == "q2" else session_b
        result = await chat.chat(q["question"], session_id=session)
        answer = result["reply"].lower()
        answered = any(sig in answer for sig in q["signals"])
        results.append({**q, "answered": answered, "answer": result["reply"][:200]})
    return {"questions": results}


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()

    from lib.settings import get_settings
    from lib.workshop import open_agent

    settings = get_settings()
    async with open_agent(args.module, settings) as chat:
        outcome = await run_eval(chat)

    expected = sum(1 for q in EVAL_QUESTIONS if q["expected_from_module"] <= args.module)
    answered = sum(1 for q in outcome["questions"] if q["answered"])
    print(f"\nEval scorecard — module {args.module}")
    print("─" * 60)
    for q in outcome["questions"]:
        mark = "✅" if q["answered"] else "❌"
        print(
            f"  {mark} [{q['id']}] (expected from module {q['expected_from_module']}) "
            f"{q['question'][:60]}…"
        )
        print(f"      → {q['answer'][:140]}")
    print("─" * 60)
    print(
        f"  {answered}/{len(EVAL_QUESTIONS)} answered · "
        f"expected ≥{expected} at module {args.module}"
    )


if __name__ == "__main__":
    asyncio.run(main())
