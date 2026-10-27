#!/usr/bin/env python3
"""make check — the pre-work and module-0 smoke test. Prints a green/red checklist."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OK, FAIL, WARN = "✅", "❌", "⚠️ "


def main() -> int:
    from lib.settings import get_settings

    s = get_settings()
    failures = 0

    def report(ok: bool, label: str, detail: str = "") -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"  {OK if ok else FAIL} {label}" + (f" — {detail}" if detail else ""))

    print("Road to Agent Memory — environment check\n")

    report(bool(s.neo4j_uri), "NEO4J_URI set", s.neo4j_uri[:40] or "missing — see .env.example")
    report(bool(s.neo4j_password), "NEO4J_PASSWORD set")
    report(bool(s.openai_api_key), "OPENAI_API_KEY set (env or personal Codespaces secret)")
    report(s.db_path.exists(), "SQLite seeded", str(s.db_path))

    if s.neo4j_uri and s.neo4j_password:
        try:
            from neo4j import GraphDatabase

            with GraphDatabase.driver(
                s.neo4j_uri, auth=(s.neo4j_username, s.neo4j_password)
            ) as driver:
                driver.verify_connectivity()
            report(True, "AuraDB reachable (Bolt)")
        except Exception as exc:  # noqa: BLE001 — report anything to the attendee
            report(False, "AuraDB reachable (Bolt)", f"{type(exc).__name__}: {exc}")

    if s.openai_api_key:
        try:
            import httpx

            resp = httpx.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {s.openai_api_key}"},
                timeout=15.0,
            )
            report(resp.status_code == 200, "OpenAI key valid", f"HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            report(False, "OpenAI key valid", str(exc))

    if s.nams_api_key:
        try:
            import httpx

            resp = httpx.get(
                f"{s.nams_base_url}/v1/conversations",
                headers={"Authorization": f"Bearer {s.nams_api_key}"},
                params={"limit": 1},
                timeout=15.0,
            )
            report(resp.status_code == 200, "NAMS key valid (module 5)", f"HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            report(False, "NAMS key valid (module 5)", str(exc))
    else:
        print(f"  {WARN} NAMS_API_KEY not set — only needed for module 5")

    print("\n" + ("All required checks passed. Try: make dev" if not failures
                  else f"{failures} check(s) failed — fix .env and re-run make check"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
