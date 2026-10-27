#!/usr/bin/env python3
"""Replay a canned scenario against a module's ChatService (in-process).

Usage: uv run scripts/run_scenario.py <name> --module N [--restart-beat] [--ablation]

--restart-beat : run the first session's first message, tear down the ChatService
                 (simulating an app restart), then continue the same session.
--ablation     : run the scenario twice — control (AGENT_REASONING_RETRIEVAL=off)
                 then treatment (on) — the module 4 proof moment (review C1).

Calls are serialized with a small pause between turns (ADR 001 rate-limit pacing).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCENARIOS = ROOT / "scripts" / "scenarios"

TURN_PAUSE_S = 1.0  # pace OpenAI calls — whole-room bursts are the risk (ADR 001)


async def run_sessions(scenario: dict, module: int, sessions: list[dict]) -> None:
    from lib.chat import ChatService
    from lib.memory import open_memory
    from lib.settings import get_settings

    get_settings.cache_clear()
    settings = get_settings()
    ontology = settings.ontology_path if module >= 3 else None
    async with open_memory(settings, module, ontology_path=ontology) as memory:
        chat = ChatService(settings, module, memory)
        for session in sessions:
            session_id = f"{scenario['name']}-{session['id']}"
            if session.get("comment"):
                print(f"\n  ── {session['comment']}")
            for text in session["messages"]:
                print(f"\n[{session_id}] customer: {text}")
                result = await chat.chat(text, session_id=session_id)
                print(f"    supportbot: {result['reply']}")
                for call in result["tool_calls"]:
                    print(f"    ↳ tool {call['name']}({json.dumps(call['input'])}) "
                          f"→ {call['duration_ms']}ms")
                used = result["context"]["summary"]
                print(f"    ◆ memory used: {used or 'none (stateless)'}")
                await asyncio.sleep(TURN_PAUSE_S)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="scenario name (scripts/scenarios/<name>.json)")
    parser.add_argument("--module", type=int, required=True)
    parser.add_argument("--restart-beat", action="store_true")
    parser.add_argument("--ablation", action="store_true")
    args = parser.parse_args()

    # Alias scenarios that reuse another's content:
    #   s3-default runs s3-ontology content with the generic POLE+O ontology
    #   s2-restart runs s2-return content with the restart beat
    aliases = {"s3-default": "s3-ontology", "s2-restart": "s2-return"}
    scenario_file = aliases.get(args.name, args.name)
    scenario = json.loads((SCENARIOS / f"{scenario_file}.json").read_text())
    print(f"=== {args.name} (module {args.module}) ===")
    print(scenario["description"])

    if args.name == "s3-default":
        os.environ["ONTOLOGY"] = "default-poleo"
    elif args.name == "s3-ontology":
        os.environ["ONTOLOGY"] = "acme_cloud"

    if args.ablation:
        for mode in ("off", "on"):
            os.environ["AGENT_REASONING_RETRIEVAL"] = mode
            print(f"\n--- ablation run: reasoning retrieval {mode.upper()} ---")
            await run_sessions(scenario, args.module, scenario["sessions"])
        return

    if args.restart_beat:
        first, rest = scenario["sessions"][0], scenario["sessions"][1:]
        head = {**first, "messages": first["messages"][:2]}
        tail = {**first, "messages": first["messages"][2:]}
        await run_sessions(scenario, args.module, [head])
        print("\n  ── APP RESTARTS (new process, same database) ──")
        await run_sessions(scenario, args.module, [tail, *rest])
        return

    await run_sessions(scenario, args.module, scenario["sessions"])


if __name__ == "__main__":
    asyncio.run(main())
