#!/usr/bin/env python3
"""make nams-check — verify the NAMS key + workspace (module 5 pre-flight)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    import httpx

    from lib.settings import get_settings

    s = get_settings()
    if not s.nams_api_key:
        print("❌ NAMS_API_KEY not set — create one at https://memory.neo4jlabs.com")
        return 1
    with httpx.Client(
        base_url=s.nams_base_url,
        headers={"Authorization": f"Bearer {s.nams_api_key}"},
        timeout=20.0,
    ) as http:
        resp = http.get("/v1/conversations", params={"limit": 1})
        if resp.status_code != 200:
            print(f"❌ NAMS auth failed: HTTP {resp.status_code} — {resp.text[:200]}")
            return 1
        caps = http.get("/v1/skills/capabilities")
        if caps.status_code == 200:
            print(f"✅ NAMS reachable; skills capabilities: {caps.json()}")
        else:
            print(f"✅ NAMS reachable (capabilities endpoint: HTTP {caps.status_code})")
            print("   ⚠️  skill distillation may be disabled on this deployment —")
            print("   if so, use the pre-distilled fallback:")
            print("   make s5-fresh-agent WITH_SKILL=fallback")
    return 0


if __name__ == "__main__":
    sys.exit(main())
