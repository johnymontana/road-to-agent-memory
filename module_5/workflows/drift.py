#!/usr/bin/env python3
"""make nams-drift: delete the memory a skill is grounded in and watch it go stale.

The downloaded provenance.json lists the memory nodes every claim and step of the
skill is grounded in. This deletes the refund-policy entities among them, then
asks NAMS for the skill's drift report: the claims and steps that lost a source.

Contrast with `make policy-change`, which edits SQLite. Governance cannot see that:
it watches the memory graph, not the system of record.
"""

from __future__ import annotations

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from module_5.workflows.nams import SKILL_DIR, call, client, read_json  # noqa: E402

# Entities whose name contains this are the refund policy the procedure relies on.
TARGET_HINT = "policy"


def grounding(provenance: dict) -> Counter:
    """How many claims and steps cite each grounding node."""
    return Counter(
        node for item in provenance["claims"] + provenance["steps"] for node in item["groundedIn"]
    )


async def grounding_entities(http, node_ids) -> list[dict]:
    """The grounding nodes that are entities (others are messages, steps, …)."""

    async def fetch(node_id):
        response = await http.get(f"/v1/entities/{node_id}")
        return response.json() if response.status_code == 200 else None

    found = await asyncio.gather(*(fetch(node_id) for node_id in node_ids))
    return [entity for entity in found if entity]


async def main() -> None:
    from lib.settings import get_settings

    skill_id = read_json(SKILL_DIR / "skill.json").get("skillId")
    provenance = read_json(SKILL_DIR / "provenance.json")
    if not skill_id or not provenance:
        sys.exit("No distilled skill found. Run make nams-seed and make nams-distill first.")
    cited = grounding(provenance)

    async with client(get_settings()) as http:
        entities = await grounding_entities(http, list(cited))
        targets = [e for e in entities if TARGET_HINT in e["name"].lower()]
        if not targets and entities:  # Otherwise, the most-cited grounding entity.
            targets = [max(entities, key=lambda e: cited[e["id"]])]
        if not targets:
            sys.exit("The skill's grounding entities are already gone. Run make nams-redistill.")

        for entity in targets:
            await call(http, "DELETE", f"/v1/entities/{entity['id']}")
            print(f"Deleted grounding entity: {entity['name']} ({entity['type']})")

        print("\nChecking skill drift…")
        report = await call(http, "GET", f"/v1/skills/{skill_id}/drift")

    claims = {c["claimId"]: c["text"] for c in provenance["claims"]}
    steps = {s["id"]: s["name"] for s in provenance["steps"]}
    stale_claims = report.get("staleClaims") or []
    stale_steps = report.get("staleSteps") or []
    print(
        f"  status: {report['status']} · {len(stale_claims)}/{report['totalClaims']} claims "
        f"and {len(stale_steps)}/{report['totalSteps']} steps lost a source"
    )
    for claim in stale_claims:
        print(f"    ⚠️  claim: {claims.get(claim['claimId'], claim['claimId'])}")
    for step in stale_steps:
        print(f"    ⚠️  step:  {steps.get(step['stepId'], step['stepId'])}")
    if report["status"] == "drifted":
        print("\nThe skill is stale: its grounding was deleted. Next: make nams-redistill")
    else:
        print("\nNo drift reported:", json.dumps(report)[:200])


if __name__ == "__main__":
    asyncio.run(main())
