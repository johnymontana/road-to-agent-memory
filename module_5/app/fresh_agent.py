"""A fresh agent with no memory that loads a distilled skill as instructions.

Every mode starts with the same business tools, base instructions and authorized
case. Loading SKILL.md adds the written procedure. The agent calls its own tools
against current SQL data and receives no conversation history or memory client.

Note: this demo calls the model directly with an authorized billing case. It skips
the per-turn guardrails (guardrails.py), but `issue_refund` still enforces SQL policy.
"""

from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from pydantic_ai import Agent

from lib.settings import AppSettings

from .agent import INSTRUCTIONS
from .tools import SQLITE_TOOLS, ToolDeps

ROOT = Path(__file__).resolve().parents[2]
INCIDENT = "ravi-duplicate-compute"
TICKET = (
    "Hi, this is Ravi Shah at Northwind Robotics (ravi.shah@northwind.example). "
    "I was double-charged $49 for Acme Cloud Compute. Can you refund me?"
)


def load_skill(mode: str) -> str | None:
    """Resolve explicit modes; missing skills must not silently become controls."""
    if mode == "off":
        return None
    if mode not in ("on", "fallback"):
        raise ValueError("Skill mode must be on, off, or fallback")
    folder = "distilled" if mode == "on" else "pre-distilled-skill"
    path = ROOT / "artifacts" / folder / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(
            f"No skill at {path}. Run make nams-distill, or use WITH_SKILL=fallback."
        )
    return path.read_text()


def create_fresh_agent(settings: AppSettings, *, skill: str | None = None) -> Agent:
    instructions = INSTRUCTIONS
    if skill is not None:
        instructions += "\n\n## Distilled procedure (from organizational memory)\n" + skill
    return Agent(
        f"openai:{settings.openai_model}",
        deps_type=ToolDeps,
        tools=list(SQLITE_TOOLS),
        output_type=str,
        instructions=instructions,
    )


async def run_fresh_agent(settings: AppSettings, *, mode: str = "on") -> dict:
    """Run the ticket once, on a private SQLite copy where the case is still open.

    The copy makes `WITH_SKILL=off` and `on` start from the same state, lets the demo be
    repeated, and never changes your workshop database.
    """
    skill = load_skill(mode)
    agent = create_fresh_agent(settings, skill=skill)
    collector: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="fresh-agent-") as folder:
        db_path = Path(folder) / "acme_cloud.db"
        if settings.db_path.exists():
            with sqlite3.connect(settings.db_path) as source, sqlite3.connect(db_path) as copy:
                source.backup(copy)
                copy.execute("DELETE FROM refunds WHERE incident_id=?", (INCIDENT,))
        result = await agent.run(
            TICKET,
            deps=ToolDeps(
                db_path=db_path if settings.db_path.exists() else settings.db_path,
                collector=collector,
                account_email="ravi.shah@northwind.example",
                incident_id=INCIDENT,
                authorize_refund=True,
            ),
        )
    return {"reply": result.output, "tool_calls": collector, "with_skill": skill is not None}
