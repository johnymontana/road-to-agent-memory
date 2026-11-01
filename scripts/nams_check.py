#!/usr/bin/env python3
"""Compatibility CLI for the module 5 check workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from module_5.workflows.check import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
