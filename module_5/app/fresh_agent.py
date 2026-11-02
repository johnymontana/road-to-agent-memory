"""A fresh business agent can load a skill without loading any prior memory."""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent

from lib.settings import AppSettings

from .agent import BASE_INSTRUCTIONS
from .tools import SQLITE_TOOLS, ToolDeps

ROOT = Path(__file__).resolve().parents[2]
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
    instructions = BASE_INSTRUCTIONS
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
    skill = load_skill(mode)
    agent = create_fresh_agent(settings, skill=skill)
    collector: list[dict] = []
    result = await agent.run(
        TICKET,
        deps=ToolDeps(
            db_path=settings.db_path,
            collector=collector,
            account_email="ravi.shah@northwind.example",
            incident_id="ravi-duplicate-compute",
            authorize_refund=True,
        ),
    )
    return {"reply": result.output, "tool_calls": collector, "with_skill": skill is not None}
