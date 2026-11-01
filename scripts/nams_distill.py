#!/usr/bin/env python3
"""Compatibility CLI for the module 5 distill workflow."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from module_5.workflows.distill import main  # noqa: E402

if __name__ == "__main__":
    asyncio.run(main(redistill="--redistill" in sys.argv))
