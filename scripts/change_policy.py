#!/usr/bin/env python3
"""make policy-change — the drift beat's first step (module 5).

Flips the Pro plan's no-approval refund limit in SQLite (the system of record).
Point of the demo: NAMS governance sees NOTHING from this — it watches the
memory graph, not your database. `make nams-drift` then deletes the policy
*entity* from memory, which governance does see.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> None:
    from lib.db import connect
    from lib.settings import get_settings

    s = get_settings()
    with connect(s.db_path) as conn:
        before = conn.execute("SELECT refund_limit FROM plans WHERE name = 'Pro'").fetchone()[
            "refund_limit"
        ]
        new_limit = 150.0 if before >= 250.0 else 250.0
        conn.execute("UPDATE plans SET refund_limit = ? WHERE name = 'Pro'", (new_limit,))
        conn.execute(
            "UPDATE policies SET body = replace(body, ?, ?), updated_at = datetime('now') "
            "WHERE topic = 'refund'",
            (f"Pro ${before:.0f}", f"Pro ${new_limit:.0f}"),
        )
        conn.commit()
    print(f"Pro plan refund limit changed in SQLite: ${before:.0f} → ${new_limit:.0f}")
    if new_limit == 250.0:
        print("Restored the workshop default. (Run it again to repeat the demo.)")
        return
    print("Note: this changed the system of record only — the memory graph (and any")
    print("distilled skill grounded in it) still references the old limit.")
    report_drift(s)
    print("That's the governance blind spot. Next: make nams-drift")


def report_drift(settings) -> None:
    """Ask NAMS whether the distilled skill noticed. It cannot: SQLite isn't memory."""
    import httpx

    from module_5.workflows.nams import SKILL_DIR, read_json

    skill_id = read_json(SKILL_DIR / "skill.json").get("skillId")
    if not (skill_id and settings.nams_api_key):
        return
    try:
        response = httpx.get(
            f"{settings.nams_base_url}/v1/skills/{skill_id}/drift",
            headers={"Authorization": f"Bearer {settings.nams_api_key}"},
            timeout=30,
        )
        response.raise_for_status()
    except httpx.HTTPError as error:
        print(f"(Could not read the skill's drift report: {error})")
        return
    print(f"NAMS drift check for the distilled skill: {response.json()['status']}")


if __name__ == "__main__":
    main()
