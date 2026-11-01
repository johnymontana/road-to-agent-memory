"""Shared HTTP transport; every lesson supplies its own complete agent factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .graph import bolt_graph
from .settings import get_settings
from .workshop import AgentFactory


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


def create_app(agent_factory: AgentFactory, *, title: str, nams_graph_reader=None) -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with agent_factory(settings) as chat:
            app.state.memory = chat.memory
            app.state.chat = chat
            yield

    app = FastAPI(title=title, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "module": app.state.chat.module,
            "memory_layers": app.state.chat.memory_layers,
        }

    @app.post("/api/chat")
    async def chat(req: ChatRequest) -> dict[str, Any]:
        return await app.state.chat.chat(req.message, req.session_id)

    @app.get("/api/graph")
    async def graph(layer: str = "all") -> dict[str, Any]:
        if app.state.memory is None:
            return {"nodes": [], "relationships": []}
        return await bolt_graph(app.state.memory, layer)

    @app.get("/api/graph/nams")
    async def graph_nams() -> dict[str, Any]:
        if nams_graph_reader is None:
            return {"nodes": [], "relationships": [], "unavailable": True}
        return await nams_graph_reader(settings)

    @app.get("/api/eval")
    async def eval_endpoint() -> dict[str, Any]:
        from scripts.eval import run_eval

        return await run_eval(app.state.chat)

    return app
