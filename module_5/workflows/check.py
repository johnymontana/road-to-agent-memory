#!/usr/bin/env python3
"""make nams-check — verify the NAMS key + workspace (module 5 pre-flight)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> int:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    fallback = "Fallback: make s5-fresh-agent WITH_SKILL=fallback"
    if not s.nams_api_key:
        print("❌ NAMS_API_KEY not set — create one at https://memory.neo4jlabs.com")
        print(fallback)
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
            print(fallback)
            return 1
        if resp.status_code != 200:
            print(f"❌ NAMS workspace check failed: HTTP {resp.status_code}")
            print(fallback)
            return 1
        try:
            caps = http.get("/v1/skills/capabilities")
        except httpx.RequestError as error:
            print(f"✅ NAMS reachable; capability check failed ({type(error).__name__}).")
            print(fallback)
            return 1
        if caps.status_code != 200:
            print(f"❌ NAMS reachable; capability check returned HTTP {caps.status_code}.")
            print(fallback)
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
            print(fallback)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
