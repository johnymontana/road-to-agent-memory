#!/usr/bin/env python3
"""make nams-check — verify the NAMS key + workspace (module 5 pre-flight).

Readings, in order: the workspace answers, distillation is enabled, the
workspace's active ontology accepts the plain entities `make nams-seed` writes,
and (when a package was downloaded) that package belongs to this workspace.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from module_5.workflows.nams import SKILL_DIR, SKILL_NAME, read_json  # noqa: E402

# Entity types the seed writes with only name + description. A workspace whose
# active ontology requires more properties on them rejects the seed (HTTP 422).
SEED_TYPES = ("person", "organization", "custom")
FALLBACK = "Fallback: make s5-fresh-agent WITH_SKILL=fallback"


def ontology_conflicts(active) -> tuple[str | None, str, list[str]]:
    """(name, validation mode, reasons the seed would be rejected) for the active ontology."""
    ontology = active.get("ontology") if isinstance(active, dict) else None
    if not isinstance(ontology, dict):
        return None, "", []
    version = active.get("version") or {}
    name = (ontology.get("domain") or {}).get("name") or version.get("ontology_id") or "custom"
    mode = str(version.get("validation_mode") or "")
    declared: dict[str, list[str]] = {}
    for entity_type in ontology.get("entity_types") or []:
        label = str(entity_type.get("label") or entity_type.get("name") or "").lower()
        properties = entity_type.get("properties") or []
        declared[label] = [p.get("name") for p in properties if p.get("required")]
    conflicts = []
    for seed_type in SEED_TYPES:
        if seed_type in declared and declared[seed_type]:
            conflicts.append(f"{seed_type} requires {', '.join(declared[seed_type])}")
        elif seed_type not in declared and mode == "strict":
            conflicts.append(f"{seed_type} is not declared (strict validation)")
    return name, mode, conflicts


def main() -> int:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    if not s.nams_api_key:
        print("❌ NAMS_API_KEY not set — create one at https://memory.neo4jlabs.com")
        print(FALLBACK)
        return 1
    with httpx.Client(
        base_url=s.nams_base_url,
        headers={"Authorization": f"Bearer {s.nams_api_key}"},
        timeout=20.0,
    ) as http:
        try:
            resp = http.get("/v1/conversations", params={"limit": 1})
        except httpx.RequestError as error:
            print(f"❌ NAMS unreachable ({type(error).__name__}). Check NAMS_BASE_URL and network.")
            print(FALLBACK)
            return 1
        if resp.status_code != 200:
            print(f"❌ NAMS workspace check failed: HTTP {resp.status_code}")
            print(FALLBACK)
            return 1
        try:
            caps = http.get("/v1/skills/capabilities")
        except httpx.RequestError as error:
            print(f"✅ NAMS reachable; capability check failed ({type(error).__name__}).")
            print(FALLBACK)
            return 1
        if caps.status_code != 200:
            print(f"❌ NAMS reachable; capability check returned HTTP {caps.status_code}.")
            print(FALLBACK)
            return 1
        try:
            gates = caps.json()
        except ValueError:
            gates = None
        if isinstance(gates, dict) and gates.get("distillation") is True:
            print(
                "✅ NAMS reachable; skill distillation enabled "
                f"(publish gates: grounding ≥ {gates.get('groundingThreshold')}, "
                f"coverage ≥ {gates.get('coverageThreshold')})"
            )
        else:
            print("❌ NAMS reachable; skill distillation is disabled or unconfirmed.")
            print(FALLBACK)
            return 1

        # The seed writes plain person/organization/custom entities. A workspace that
        # another project configured with its own ontology can reject them.
        try:
            active = http.get("/v1/ontologies/active")
            name, mode, conflicts = ontology_conflicts(
                active.json() if active.status_code == 200 else None
            )
        except (httpx.RequestError, ValueError) as error:
            name, mode, conflicts = None, "", []
            print(f"⚠️  Could not read the active ontology ({type(error).__name__}).")
        if conflicts:
            reasons = "; ".join(conflicts)
            print(f"❌ Active ontology '{name}' would reject make nams-seed: {reasons}.")
            print(
                "   Point NAMS_API_KEY at a workshop workspace without a custom ontology "
                "(create one at https://memory.neo4jlabs.com/dashboard/api-keys)."
            )
            print(FALLBACK)
            return 1
        if name:
            print(f"✅ Active ontology '{name}'{f' ({mode})' if mode else ''} accepts the seed")
        else:
            print("✅ Default ontology; the workshop seed is accepted")

        # Is there already a distilled skill here, and is the downloaded package from here?
        receipt = read_json(SKILL_DIR / "skill.json")
        try:
            listing = http.get("/v1/skills")
            skills = listing.json().get("skills", []) if listing.status_code == 200 else []
            named = [sk for sk in skills if sk.get("name") == SKILL_NAME]
            if named:
                statuses = ", ".join(sorted({str(sk.get("status")) for sk in named}))
                print(f"✅ Workspace skill {SKILL_NAME}: {statuses}")
            else:
                print(
                    f"ℹ️  No {SKILL_NAME} skill in this workspace yet "
                    "(make nams-seed, then make nams-distill)"
                )
            if receipt.get("skillId"):
                found = http.get(f"/v1/skills/{receipt['skillId']}")
                version = receipt.get("versionId", "?")
                if found.status_code == 200:
                    print(f"✅ Downloaded package {version} belongs to this workspace")
                else:
                    local = SKILL_DIR.is_relative_to(ROOT)
                    where = SKILL_DIR.relative_to(ROOT) if local else SKILL_DIR
                    print(
                        f"⚠️  The downloaded package in {where}/ is not in "
                        f"this workspace (HTTP {found.status_code}). WITH_SKILL=on still reads it "
                        "locally; the NAMS graph view and drift need the workspace that produced "
                        "it, or a new make nams-seed + make nams-distill here."
                    )
        except (httpx.RequestError, ValueError) as error:
            print(f"⚠️  Could not list this workspace's skills ({type(error).__name__}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
