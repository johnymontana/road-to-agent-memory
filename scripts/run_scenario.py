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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCENARIOS = ROOT / "scripts" / "scenarios"

TURN_PAUSE_S = 1.0  # pace OpenAI calls — whole-room bursts are the risk (ADR 001)


async def run_sessions(scenario: dict, module: int, sessions: list[dict], **options) -> None:
    from lib.settings import get_settings
    from lib.workshop import open_agent

    get_settings.cache_clear()
    settings = get_settings()
    async with open_agent(module, settings, **options) as chat:
        for session in sessions:
            session_id = f"{scenario['name']}-{session['id']}"
            if session.get("comment"):
                print(f"\n  ── {session['comment']}")
            for text in session["messages"]:
                print(f"\n[{session_id}] customer: {text}")
                result = await chat.chat(text, session_id=session_id)
                print(f"    supportbot: {result['reply']}")
                for call in result["tool_calls"]:
                    print(
                        f"    ↳ tool {call['name']}({json.dumps(call['input'])}) "
                        f"→ {call['duration_ms']}ms"
                    )
                used = result["context"]["summary"]
                print(f"    ◆ memory used: {used or 'none (stateless)'}")
                await asyncio.sleep(TURN_PAUSE_S)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="scenario name (scripts/scenarios/<name>.json)")
    parser.add_argument("--module", type=int, choices=range(1, 6), required=True)
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

    options = {}
    if args.name == "s3-default":
        options["ontology"] = "default-poleo"
    elif args.name == "s3-ontology":
        options["ontology"] = "acme_cloud"

    if args.ablation:
        if args.module not in (4, 5):
            parser.error("--ablation requires module 4 or 5")
        for mode in ("off", "on"):
            options["reasoning_retrieval"] = mode == "on"
            print(f"\n--- ablation run: reasoning retrieval {mode.upper()} ---")
            await run_sessions(scenario, args.module, scenario["sessions"], **options)
        return

    if args.restart_beat:
        first, rest = scenario["sessions"][0], scenario["sessions"][1:]
        head = {**first, "messages": first["messages"][:2]}
        tail = {**first, "messages": first["messages"][2:]}
        await run_sessions(scenario, args.module, [head], **options)
        print("\n  ── APP STATE RECREATED (new agent/client, same process and database) ──")
        await run_sessions(scenario, args.module, [tail, *rest], **options)
        return

    await run_sessions(scenario, args.module, scenario["sessions"], **options)


if __name__ == "__main__":
    asyncio.run(main())
