"""FastAPI app factory — every module_N/app/main.py calls create_app(N).
Endpoints implement docs/frontend-contract.md."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .chat import ChatService
from .graph import bolt_graph, nams_graph
from .memory import open_memory
from .settings import get_settings


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


def create_app(module: int) -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        ontology = settings.ontology_path if module >= 3 else None
        async with open_memory(settings, module, ontology_path=ontology) as memory:
            app.state.memory = memory
            app.state.chat = ChatService(settings, module, memory)
            yield

    app = FastAPI(title=f"SupportBot — module {module}", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "module": module,
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
        return await nams_graph(settings)

    @app.get("/api/eval")
    async def eval_endpoint() -> dict[str, Any]:
        from scripts.eval import run_eval

        return await run_eval(app.state.chat)

    return app
