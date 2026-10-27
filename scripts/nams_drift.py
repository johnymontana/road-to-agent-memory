#!/usr/bin/env python3
"""make nams-drift — the drift beat (module 5, decision D4).

Deletes the refund-policy entity from the workspace memory. The distilled
skill's GROUNDED_IN claims lose their source nodes, and governance flags the
skill as stale. Contrast with `make policy-change` (SQLite), which governance
cannot see — it watches the memory graph, not the system of record.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


async def main() -> None:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    headers = {"Authorization": f"Bearer {s.nams_api_key}"}
    async with httpx.AsyncClient(
        base_url=s.nams_base_url, headers=headers, timeout=30.0
    ) as http:
        # Find the policy/plan entity whose facts ground the refund skill.
        resp = await http.post("/v1/entities/search", json={"query": "Pro plan refund limit"})
        resp.raise_for_status()
        entities = resp.json().get("entities", [])
        if not entities:
            print("No policy entity found — run make nams-seed first.")
            sys.exit(1)
        target = entities[0]
        print(f"Deleting grounding entity: {target.get('name')} ({target.get('type')})")
        resp = await http.delete(f"/v1/entities/{target['id']}")
        resp.raise_for_status()

        print("\nChecking skill drift…")
        skills = (await http.get("/v1/skills")).json().get("skills", [])
        for skill in skills:
            drift = await http.get(f"/v1/skills/{skill['id']}/drift")
            if drift.status_code != 200:
                continue
            report = drift.json()
            flagged = report.get("flagged_claims") or report.get("claims") or []
            print(f"  skill '{skill.get('name')}': {len(flagged)} claim(s) lost grounding")
            for claim in flagged[:5]:
                print(f"    ⚠️  {claim}")
        print("\nThe skill is stale — its grounding was deleted. Next: make nams-redistill")


if __name__ == "__main__":
    asyncio.run(main())
