#!/usr/bin/env python3
"""make nams-distill / nams-redistill — distill a grounded skill from the seeded
reasoning memory, publish it, and download SKILL.md to artifacts/distilled/.

--redistill: run after `make nams-drift`; diffs the new SKILL.md against the
previous download.
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "artifacts" / "distilled"
POLL_S = 5
TIMEOUT_S = 600


async def main(redistill: bool) -> None:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    headers = {"Authorization": f"Bearer {s.nams_api_key}"}
    async with httpx.AsyncClient(base_url=s.nams_base_url, headers=headers, timeout=30.0) as http:
        print("Triggering skill distillation over the refund-procedure memory…")
        resp = await http.post(
            "/v1/skills/generate",
            json={
                "name": "acme-refund-procedure",
                "scope": {"taskContains": "Refund"},
            },
        )
        resp.raise_for_status()
        run_id = resp.json().get("runId") or resp.json().get("id")

        deadline = time.monotonic() + TIMEOUT_S
        skill_id = None
        while time.monotonic() < deadline:
            await asyncio.sleep(POLL_S)
            run_response = await http.get(f"/v1/skills/runs/{run_id}")
            run_response.raise_for_status()
            run = run_response.json()
            status = run.get("status", "unknown")
            print(f"  …run {run_id}: {status}")
            if status in ("completed", "succeeded", "done"):
                skill_id = run.get("skillId") or run.get("skill_id")
                break
            if status in ("failed", "error"):
                print(f"Distillation failed: {run}")
                print(
                    "Fallback: make s5-fresh-agent WITH_SKILL=fallback "
                    "uses artifacts/pre-distilled-skill/SKILL.md"
                )
                sys.exit(1)
        if not skill_id:
            print("Timed out waiting for distillation — use the pre-distilled fallback.")
            sys.exit(1)

        pub = await http.post(f"/v1/skills/{skill_id}/publish")
        if pub.status_code == 409:
            print("  …publish gated pending review; approving and retrying")
            review = await http.post(f"/v1/skills/{skill_id}/review", json={"action": "approve"})
            review.raise_for_status()
            pub = await http.post(f"/v1/skills/{skill_id}/publish")
        pub.raise_for_status()

        dl = await http.get(f"/v1/skills/{skill_id}/download")
        dl.raise_for_status()
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        skill_md = OUT_DIR / "SKILL.md"
        previous = skill_md.read_text() if skill_md.exists() else None
        skill_md.write_text(dl.text)
        print(f"\nSkill published and downloaded → {skill_md}")
        if redistill and previous and previous != dl.text:
            print("\n── diff vs. previous distillation ──")
            import difflib

            for line in difflib.unified_diff(
                previous.splitlines(), dl.text.splitlines(), lineterm="", n=2
            ):
                print(line)
        print("\nNext: make s5-fresh-agent   (fresh agent resolves the ticket cold)")


if __name__ == "__main__":
    asyncio.run(main(redistill="--redistill" in sys.argv))
