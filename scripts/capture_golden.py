#!/usr/bin/env python3
"""Capture a bounded session graph as evidence, not self-validating test assertions."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


async def main(module, session):
    from lib.graph import bolt_graph
    from lib.settings import get_settings
    from lib.workshop import open_agent

    settings = get_settings()
    async with open_agent(module, settings) as agent:
        graph = (
            await bolt_graph(agent.memory, session_id=session)
            if agent.memory
            else {"nodes": [], "relationships": []}
        )
    output = settings.data_dir / "snapshots"
    output.mkdir(parents=True, exist_ok=True)
    from uuid import uuid4

    path = output / f"{uuid4().hex}.json"
    path.write_text(
        json.dumps(
            {
                "module": module,
                "session_id": session,
                "source": "actual scoped graph; verify learning invariants separately",
                "graph": graph,
            },
            indent=2,
        )
    )
    print(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", type=int, choices=range(1, 5), required=True)
    parser.add_argument("--session", required=True)
    args = parser.parse_args()
    asyncio.run(main(args.module, args.session))
