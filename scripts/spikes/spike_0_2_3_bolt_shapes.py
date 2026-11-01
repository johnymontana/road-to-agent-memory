#!/usr/bin/env python3
"""Phase 0 spike 0.2 + 0.3 — Bolt get_context shape (F1) and add_message
return shape (F5, hydration hook contract). Writes findings to stdout;
results recorded in docs/verification-log.md."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

SESSION = "spike-02-03"


async def main() -> None:
    from lib.settings import get_settings
    from module_2.app.memory import open_memory

    settings = get_settings()
    async with open_memory(settings) as memory:
        assert memory is not None
        print("== SPIKE 0.3: add_message return shape ==")
        msg = await memory.short_term.add_message(
            SESSION,
            "user",
            "Hi, I'm Maya Chen from Northwind Robotics, on the Pro plan. "
            "We use Acme Cloud Compute and were double-charged $49.",
        )
        print(f"type: {type(msg).__name__}")
        fields = msg.model_dump() if hasattr(msg, "model_dump") else vars(msg)
        print(f"fields: {sorted(fields.keys())}")
        print(f"id available: {getattr(msg, 'id', None) is not None}")

        print("\n== SPIKE 0.2: get_context shape on Bolt ==")
        ctx = await memory.get_context("What did we discuss?", session_id=SESSION)
        print(f"return type: {type(ctx).__name__}")
        print(f"--- context ({len(str(ctx))} chars) ---")
        print(str(ctx)[:800])
        print("--- end ---")

        # Do reflections/observations tiers exist on Bolt?
        for method in ("get_reflections", "get_observations"):
            fn = getattr(memory.short_term, method, None)
            if fn is None:
                print(f"{method}: NOT PRESENT on Bolt short_term")
                continue
            try:
                out = await fn(SESSION)
                print(f"{method}: OK -> {type(out).__name__}, {len(out)} item(s)")
            except Exception as exc:  # noqa: BLE001
                print(f"{method}: raises {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
