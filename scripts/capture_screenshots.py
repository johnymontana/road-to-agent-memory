#!/usr/bin/env python3
"""Capture the actual running backend module; never select a module with a URL query.

Start make dev MODULE=N first. Usage: uv run scripts/capture_screenshots.py --module N
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]


async def main(module):
    from playwright.async_api import async_playwright

    async with httpx.AsyncClient() as http:
        health = (await http.get("http://localhost:8000/api/health")).raise_for_status().json()
    if health["module"] != module:
        raise SystemExit(
            f"Expected module {module}, running {health['module']}. "
            "Stop the old server and launch the requested module."
        )
    output = ROOT / "artifacts" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 1000})
        await page.goto("http://localhost:5173")
        await page.wait_for_function("!document.querySelector('.starting-banner')")
        await page.get_by_label("Graph view").select_option("all")
        await page.wait_for_timeout(3000)
        assert f"Module {module}" in await page.locator(".chat-panel").inner_text()
        await page.screenshot(path=output / f"module-{module}-live.png")
        (output / f"module-{module}-live.json").write_text(
            json.dumps(
                {"health": health, "source": "actual running backend; all stored memory view"},
                indent=2,
            )
        )
        await browser.close()
    print(f"Captured verified module {module}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, type=int, choices=range(1, 5))
    asyncio.run(main(parser.parse_args().module))
