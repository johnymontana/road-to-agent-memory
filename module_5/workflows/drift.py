#!/usr/bin/env python3
"""make nams-drift: remove the seeded policy that grounds this published skill.

An instructor's disposable-workspace demo. The seed receipt identifies the policy
and its isolated user scope. The skill receipt and provenance identify the evidence
and published version. If they disagree, the demo stops before deleting anything.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from module_5.workflows.nams import SKILL_DIR, call, client, read_json, seed_state_path  # noqa: E402
from module_5.workflows.seed import POLICY_NAME  # noqa: E402


async def main() -> None:
    from lib.settings import get_settings

    settings = get_settings()
    seed = read_json(seed_state_path(settings))
    receipt = read_json(SKILL_DIR / "skill.json")
    provenance = read_json(SKILL_DIR / "provenance.json")
    policy_id = seed.get("policyEntityId")
    skill_id = receipt.get("skillId")
    version_id = receipt.get("versionId")
    if not all((policy_id, seed.get("userId"), skill_id, version_id, receipt.get("runId"))):
        sys.exit("Drift needs new receipts. Run make nams-seed and make nams-distill.")
    if (
        not seed.get("conversationId")
        or seed["conversationId"] != receipt.get("conversationId")
        or provenance.get("distillationRun") != receipt["runId"]
    ):
        sys.exit("Receipts differ. Run make nams-distill for the current seed.")
    evidence = provenance.get("claims", []) + provenance.get("steps", [])
    cited = {node for item in evidence for node in item.get("groundedIn", [])}

    async with client(settings) as http:
        details = await call(http, "GET", f"/v1/skills/{skill_id}")
        if details.get("skill", {}).get("publishedVersionId") != version_id:
            sys.exit("The published version has changed. Inspect the current package before drift.")
        conversation = await call(http, "GET", f"/v1/conversations/{seed['conversationId']}")
        if conversation.get("userId") != seed["userId"]:
            sys.exit("Could not verify this seed's hosted conversation. Skip deletion.")
        # Extracted representations of the policy can have different IDs and types
        # from the explicit seed. Resolve only within this run's dedicated user scope.
        response = await http.get("/v1/entities", params={"userId": seed["userId"], "limit": 200})
        response.raise_for_status()
        policies = [
            entity
            for entity in response.json().get("entities", [])
            if entity.get("userId") == seed["userId"] and entity.get("name") == POLICY_NAME
        ]
        if not any(entity["id"] == policy_id for entity in policies):
            sys.exit("Could not verify the refund policy in this seed's scope. Skip deletion.")
        targets = [entity for entity in policies if entity["id"] in cited]
        if not targets:
            sys.exit("No cited refund policy remains in this seed. Skip deletion or re-distill.")
        for entity in sorted(targets, key=lambda e: e["id"] == policy_id):
            await call(http, "DELETE", f"/v1/entities/{entity['id']}")
            print(f"Deleted grounding entity: {entity['name']} ({entity['type']}, {entity['id']})")
        print("\nChecking skill drift…")
        response = await http.get(f"/v1/skills/{skill_id}/drift", params={"version": version_id})
        response.raise_for_status()
        report = response.json()

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
