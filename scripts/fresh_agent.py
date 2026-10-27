#!/usr/bin/env python3
"""make s5-fresh-agent — the module 5 payoff.

A FRESH agent (no session history, no traces) resolves a refund ticket cold.
WITH_SKILL=on (default): the distilled SKILL.md is loaded into its instructions.
WITH_SKILL=off: control run without the skill (the ablation pair — review C2).
WITH_SKILL=fallback: use the checked-in pre-distilled skill (B2 fallback).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TICKET = (
    "Hi, this is Ravi Shah at Northwind Robotics (ravi.shah@northwind.example). "
    "I was double-charged $49 for Acme Cloud Compute. Can you refund me?"
)


async def main(with_skill: str) -> None:
    from pydantic_ai import Agent

    from lib.chat import BASE_INSTRUCTIONS
    from lib.settings import get_settings
    from lib.tools import SQLITE_TOOLS, ToolDeps

    settings = get_settings()
    instructions = BASE_INSTRUCTIONS
    skill_path = None
    if with_skill == "on":
        skill_path = ROOT / "artifacts" / "distilled" / "SKILL.md"
    elif with_skill == "fallback":
        skill_path = ROOT / "artifacts" / "pre-distilled-skill" / "SKILL.md"
    if skill_path is not None:
        if not skill_path.exists():
            print(f"No skill at {skill_path} — run make nams-distill first "
                  "(or WITH_SKILL=fallback).")
            sys.exit(1)
        instructions += (
            "\n\n## Distilled procedure (from organizational memory)\n"
            + skill_path.read_text()
        )
        print(f"Fresh agent WITH distilled skill ({skill_path.name})")
    else:
        print("Fresh agent WITHOUT skill (control run)")

    agent = Agent(
        f"openai:{settings.openai_model}",
        deps_type=ToolDeps,
        tools=list(SQLITE_TOOLS),
        output_type=str,
        instructions=instructions,
    )
    collector: list[dict] = []
    result = await agent.run(TICKET, deps=ToolDeps(db_path=settings.db_path,
                                                   collector=collector))
    print(f"\ncustomer: {TICKET}")
    print(f"agent:    {result.output}")
    print("\ntool calls:")
    for call in collector:
        print(f"  ↳ {call['name']} → {str(call['output'])[:120]}")
    print("\nCompare against the control run: WITH_SKILL=off "
          "uv run scripts/fresh_agent.py")


if __name__ == "__main__":
    # WITH_SKILL env var wins; CLI flag --with-skill X also accepted.
    import os

    mode = os.environ.get("WITH_SKILL", "on")
    if "--with-skill" in sys.argv:
        mode = sys.argv[sys.argv.index("--with-skill") + 1]
    asyncio.run(main(mode))
