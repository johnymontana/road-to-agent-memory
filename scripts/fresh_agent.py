#!/usr/bin/env python3
"""CLI for module_5/app/fresh_agent.py; keep the participant make target stable."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.settings import get_settings  # noqa: E402
from module_5.app.fresh_agent import TICKET, run_fresh_agent  # noqa: E402


async def main(mode: str) -> None:
    try:
        result = await run_fresh_agent(get_settings(), mode=mode)
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc
    label = {
        "off": "WITHOUT skill (control)",
        "on": "WITH downloaded NAMS skill",
        "fallback": "WITH checked-in fallback skill",
    }[mode]
    print(f"Fresh agent {label}\n\ncustomer: {TICKET}\nagent: {result['reply']}")
    print("\ntool calls (in order):")
    for call in result["tool_calls"]:
        output = call["output"]
        status = output.get("status") if isinstance(output, dict) else None
        print(f"  ↳ {call['name']}" + (f" → {status}" if status else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--with-skill",
        choices=("on", "off", "fallback"),
        default=os.environ.get("WITH_SKILL", "on"),
    )
    asyncio.run(main(parser.parse_args().with_skill))
