#!/usr/bin/env python3
"""make nams-distill / nams-redistill: distill a skill from the seeded refund history.

1. POST /v1/skills/generate starts a distillation run scoped to the conversation
   that `make nams-seed` wrote.
2. Poll GET /v1/skills/runs/{id} until it succeeds (about a minute).
3. Approve (the human-review gate), then publish the new version.
4. Download the skill package (a zip) into artifacts/distilled/: SKILL.md,
   references/ and provenance.json (which memory each claim is grounded in).

--redistill: run after `make nams-drift`. It distills a new version of the same
skill from the current graph and diffs the new SKILL.md against the old one.
"""

from __future__ import annotations

import asyncio
import difflib
import io
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from module_5.workflows.nams import (  # noqa: E402
    SKILL_DIR,
    SKILL_NAME,
    call,
    client,
    read_json,
    seed_state_path,
    write_json,
)

OUT_DIR = SKILL_DIR
POLL_S = 5
TIMEOUT_S = 600
FINISHED = ("succeeded", "failed", "error", "cancelled")
FALLBACK = "Fallback: make s5-fresh-agent WITH_SKILL=fallback (artifacts/pre-distilled-skill)."


async def wait_for_run(http, run_id: str) -> dict:
    """Poll a run, printing each status change (queued → … → succeeded)."""
    deadline = time.monotonic() + TIMEOUT_S
    last = None
    while time.monotonic() < deadline:
        run = await call(http, "GET", f"/v1/skills/runs/{run_id}")
        if run["status"] != last:
            last = run["status"]
            print(f"  …{last} ({run.get('progress', 0)}%)")
        if run["status"] in FINISHED or run.get("error") or run.get("failCode"):
            return run
        await asyncio.sleep(POLL_S)
    return {"status": "timeout", "error": f"no result after {TIMEOUT_S}s"}


def unpack(package: bytes, destination: Path) -> str:
    """Extract the skill zip (one top-level folder) into destination; return SKILL.md."""
    with zipfile.ZipFile(io.BytesIO(package)) as archive:
        for member in archive.infolist():
            parts = PurePosixPath(member.filename).parts[1:]  # drop "<skill-name>/"
            if member.is_dir() or not parts or ".." in parts:
                continue
            target = destination.joinpath(*parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    return (destination / "SKILL.md").read_text()


def print_diff(old: str, new: str) -> None:
    """Show changed procedure text; summarize the long evidence-ID lines instead."""

    def readable(text):
        return [line for line in text.splitlines() if "_evidence:" not in line]

    for line in difflib.unified_diff(readable(old), readable(new), lineterm="", n=1):
        print(line)
    old_ids = [line for line in old.splitlines() if "_evidence:" in line]
    new_ids = [line for line in new.splitlines() if "_evidence:" in line]
    changed = sum(a != b for a, b in zip(old_ids, new_ids, strict=False)) + abs(
        len(old_ids) - len(new_ids)
    )
    if changed:
        print(f"(evidence IDs changed for {changed} step(s); see provenance.json)")


async def main(redistill: bool) -> None:
    from lib.settings import get_settings

    settings = get_settings()
    seeded = read_json(seed_state_path(settings))
    if seeded.get("conversationId"):
        scope = {"type": "conversations", "conversationIds": [seeded["conversationId"]]}
    else:
        print("No seed record found (run make nams-seed); distilling the whole workspace.")
        scope = {"type": "workspace"}
    request = {"nameHint": SKILL_NAME, "scope": scope}
    previous = (OUT_DIR / "SKILL.md").read_text() if (OUT_DIR / "SKILL.md").exists() else None

    async with client(settings) as http:
        # A published name is unique per workspace, so a rerun (or --redistill)
        # distills a new version of the existing skill instead of a second skill.
        listing = await call(http, "GET", "/v1/skills")
        named = [s for s in listing.get("skills", []) if s["name"] == SKILL_NAME]
        existing = next(
            (s for s in named if s["status"] == "published"), named[0] if named else None
        )
        if existing:
            request["skillId"] = existing["id"]
        elif redistill:
            sys.exit("No distilled skill to update. Run make nams-distill first.")
        what = "a new version of the skill" if existing else "a skill"
        print(f"Distilling {what} from the seeded refund history…")
        started = await call(http, "POST", "/v1/skills/generate", request)
        run = await wait_for_run(http, started["runId"])
        if run["status"] != "succeeded":
            print(f"Distillation did not succeed: {run.get('error') or run['status']}")
            print(FALLBACK)
            sys.exit(1)
        skill_id = run["skillId"]
        print(
            f"Skill {skill_id}: grounding {run['groundingScore']:.2f}, "
            f"coverage {run['coverageScore']:.2f}"
        )

        # Human-review gate: publishing requires an approved version.
        await call(
            http,
            "POST",
            f"/v1/skills/{skill_id}/review",
            {"decision": "approve", "feedback": "Approved during the workshop."},
        )
        await call(http, "POST", f"/v1/skills/{skill_id}/publish")
        print("  …approved and published")

        package = await http.get(f"/v1/skills/{skill_id}/download")
        package.raise_for_status()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    skill_md = unpack(package.content, OUT_DIR)
    write_json(
        OUT_DIR / "skill.json",
        {"skillId": skill_id, "versionId": run.get("skillVersionId"), "runId": run["id"]},
    )
    print(f"\nDownloaded → {OUT_DIR}/SKILL.md (+ references/, provenance.json)")
    if redistill and previous is not None:
        if previous == skill_md:
            print("\nThe re-distilled SKILL.md is unchanged.")
        else:
            print("\n── diff vs. previous distillation ──")
            print_diff(previous, skill_md)
    print("\nNext: make s5-fresh-agent WITH_SKILL=on   (a fresh agent with no memory)")


if __name__ == "__main__":
    asyncio.run(main(redistill="--redistill" in sys.argv))
