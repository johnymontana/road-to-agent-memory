#!/usr/bin/env python3
"""Capture expected-graph screenshots (deck v0.9 → v1.0, module READMEs).

Requires the app running (make dev MODULE=N) and playwright browsers installed
(`uv run playwright install chromium`). Writes artifacts/screenshots/<name>.png.
Optional tooling — screenshots can also be captured by hand during rehearsal.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "screenshots"

SHOTS = {
    "m1-stateless": "1",
    "m2-message-chains": "2",
    "m3-ontology-graph": "3",
    "m4-trace-subgraph": "4",
    "m5-skill-subgraph": "5",
}


async def main() -> None:
    from playwright.async_api import async_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for name, module in SHOTS.items():
            page = await browser.new_page(viewport={"width": 1600, "height": 1000})
            await page.goto(f"http://localhost:5173/?module={module}")
            await page.wait_for_timeout(3000)  # let the graph panel fetch + settle
            await page.locator(".graph-panel").screenshot(path=OUT / f"{name}.png")
            print(f"captured {name}.png")
            await page.close()
        await browser.close()


if __name__ == "__main__":
    if "install" in sys.argv:
        raise SystemExit("Run: uv run playwright install chromium")
    asyncio.run(main())
