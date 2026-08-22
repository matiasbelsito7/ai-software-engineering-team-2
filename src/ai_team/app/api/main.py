"""
AI Software Engineering Team - FastAPI application.

Run with:
    uvicorn ai_team.app.api.main:app --reload
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from ai_team.app.api.lifespan import lifespan
from ai_team.infrastructure.config.app import AppSettings

if TYPE_CHECKING:
    from ai_team.graph.state import GraphState

logger = logging.getLogger(__name__)

settings = AppSettings()

# =====================================================================
# API schemas
# =====================================================================


class TaskRequest(BaseModel):
    """Request body for the /tasks endpoint."""

    model_config = ConfigDict(extra="forbid")

    task: str

    system_prompt: str | None = None


class AgentResultResponse(BaseModel):
    """Single agent result inside a TaskResponse."""

    model_config = ConfigDict(from_attributes=True)

    success: bool
    output: Any = None
    message: str | None = None
    next_agent: str | None = None


class TaskResponse(BaseModel):
    """Response body for a completed task."""

    model_config = ConfigDict(extra="forbid")

    task_id: str

    status: str

    results: list[AgentResultResponse] = Field(
        default_factory=list,
    )

    files: dict[str, str] = Field(
        default_factory=dict,
    )


class HealthResponse(BaseModel):
    """Health check response."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"


# =====================================================================
# Application
# =====================================================================

app = FastAPI(
    title="AI Software Engineering Team",
    version=settings.version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
    allow_credentials=settings.allow_credentials,
)


# =====================================================================
# Routes
# =====================================================================


@app.get(f"{settings.api_prefix}/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""

    return HealthResponse()


@app.post(f"{settings.api_prefix}/tasks", response_model=TaskResponse)
async def run_task(
    request: TaskRequest,
    raw: Request,
) -> TaskResponse:
    """
    Submit a task and wait for the full agent workflow to complete.
    """

    from uuid import uuid4 as _uuid4

    task_id = str(_uuid4())

    graph: Any = raw.app.state.graph

    initial = _build_initial_state(
        task=request.task,
        system_prompt=request.system_prompt,
    )

    try:
        final_state: GraphState = await graph.ainvoke(initial)
    except Exception as exc:
        logger.exception("Graph execution failed")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    return _state_to_response(
        task_id=task_id,
        state=final_state,
    )


@app.get(f"{settings.api_prefix}/tasks/{{task_id}}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    raw: Request,
) -> TaskResponse:
    """
    Placeholder: retrieve a previously run task.

    Currently runs a no-op since there is no persistence yet.
    """

    raise HTTPException(
        status_code=501,
        detail="Task persistence is not yet implemented.",
    )


# =====================================================================
# Helpers
# =====================================================================


def _build_initial_state(
    *,
    task: str,
    system_prompt: str | None,
) -> dict[str, Any]:
    """Build the initial GraphState dict for the graph."""

    return {
        "conversation": {
            "user_request": task,
            "system_prompt": system_prompt,
        },
        "execution": {},
        "artifacts": {},
    }


def _state_to_response(
    *,
    task_id: str,
    state: Any,
) -> TaskResponse:
    """Convert a final GraphState into a TaskResponse."""

    results = [
        AgentResultResponse(
            success=r.success,
            output=r.output,
            message=r.message,
            next_agent=r.next_agent,
        )
        for r in state.artifacts.results
    ]

    return TaskResponse(
        task_id=task_id,
        status="completed",
        results=results,
        files=state.artifacts.shared_files,
    )
