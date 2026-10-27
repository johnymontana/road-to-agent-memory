"""SupportBot — module 3 entry point.

The per-module diff is the workshop: compare this file across module folders
(diff module_2/app/main.py module_3/app/main.py) to see each memory layer land.
"""

import os
import sys
from pathlib import Path

# Repo root on sys.path so `lib` resolves when run as a script or module.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

os.environ.setdefault("MODULE", "3")

from lib.app_factory import create_app  # noqa: E402

app = create_app(module=3)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
