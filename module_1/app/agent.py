"""Module 1: business tools without persistent memory.

This is a complete lesson snapshot; it deliberately duplicates earlier modules.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from pydantic_ai import Agent

from lib.settings import AppSettings

from .tools import SQLITE_TOOLS, ToolDeps

BASE_INSTRUCTIONS = """You are SupportBot, the Acme Cloud customer support agent.

Help customers with billing, product questions, service status, and refunds.
Use the tools to look up real data — never invent account details, prices,
or policies. Keep answers short and concrete.
"""


class ChatService:
    """The complete support-agent loop for module 1."""

    module = 1

    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.memory = None
        tools = list(SQLITE_TOOLS)
        self.base_instructions = BASE_INSTRUCTIONS
        self.agent: Agent[ToolDeps, str] = Agent(
            f"openai:{settings.openai_model}",
            deps_type=ToolDeps,
            tools=tools,
            output_type=str,
            instructions=self.base_instructions,
        )

    @property
    def memory_layers(self) -> list[str]:
        return []

    async def chat(self, message: str, session_id: str | None = None) -> dict[str, Any]:
        session_id = session_id or f"support-m1-{uuid4().hex[:8]}"
        collector: list[dict[str, Any]] = []
        deps = ToolDeps(db_path=self.settings.db_path, collector=collector)
        memory_used: list[str] = []
        instructions = self.base_instructions

        result = await self.agent.run(message, deps=deps, instructions=instructions)
        reply = result.output

        return {
            "reply": reply,
            "session_id": session_id,
            "tool_calls": collector,
            "context": {
                "used_memory": bool(memory_used),
                "summary": ", ".join(memory_used) if memory_used else None,
            },
        }


@asynccontextmanager
async def open_agent(settings: AppSettings):
    """Construct this module’s agent and own its connection lifetime."""
    yield ChatService(settings)
