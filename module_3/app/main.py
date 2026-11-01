"""Run module 3: make dev MODULE=3. Agent construction is local to this folder."""

import sys
from pathlib import Path

# Support both python -m module_3.app.main and direct script execution.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.app_factory import create_app  # noqa: E402
from module_3.app.agent import open_agent  # noqa: E402

app = create_app(open_agent, title="SupportBot — module 3")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
