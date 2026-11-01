"""Select a lesson implementation without implementing any agent behavior."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from importlib import import_module
from typing import TYPE_CHECKING, Any, Protocol

from .settings import AppSettings, get_settings

if TYPE_CHECKING:
    from neo4j_agent_memory import MemoryClient


class WorkshopAgent(Protocol):
    module: int
    memory: MemoryClient | None

    @property
    def memory_layers(self) -> list[str]: ...

    async def chat(self, message: str, session_id: str | None = None) -> dict[str, Any]: ...


AgentFactory = Callable[[AppSettings], AbstractAsyncContextManager[WorkshopAgent]]


def load_agent_module(module: int):
    if type(module) is not int or module not in range(1, 6):
        raise ValueError("Workshop module must be an integer from 1 to 5")
    return import_module(f"module_{module}.app.agent")


@asynccontextmanager
async def open_agent(module: int, settings: AppSettings | None = None, **options):
    """CLI selection only; each lesson owns its constructor and connection lifetime."""
    implementation = load_agent_module(module)
    async with implementation.open_agent(settings or get_settings(), **options) as agent:
        yield agent
