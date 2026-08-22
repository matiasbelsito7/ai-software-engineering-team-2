"""
Tasks router.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, BackgroundTasks, Request

from ai_team.app.api.exceptions.errors import TaskNotFoundError
from ai_team.app.api.schemas.tasks import (
    AgentResultResponse,
    CreateTaskRequest,
    TaskListResponse,
    TaskResponse,
)

if TYPE_CHECKING:
    from ai_team.app.api.task_store import TaskStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])

AGENT_ORDER = [
    "planner",
    "architect",
    "backend",
    "frontend",
    "reviewer",
    "qa",
    "documentation",
    "devops",
    "git",
]


def _get_task_store(request: Request) -> TaskStore:
    return request.app.state.task_store  # type: ignore[no-any-return]


def _build_initial_state(
    *,
    task: str,
    system_prompt: str | None,
) -> dict[str, Any]:
    return {
        "conversation": {
            "user_request": task,
            "system_prompt": system_prompt,
        },
        "execution": {},
        "artifacts": {},
    }


def _state_to_results(
    state: Any,
) -> tuple[list[AgentResultResponse], dict[str, str]]:
    results = [
        AgentResultResponse(
            agent=r.metadata.get("agent", "") if r.metadata else "",
            success=r.success,
            output=r.output,
            message=r.message,
            next_agent=r.next_agent,
            metadata=r.metadata if r.metadata else {},
        )
        for r in state.artifacts.results
    ]

    files = state.artifacts.shared_files

    return results, files


async def _run_task_background(
    *,
    task_store: TaskStore,
    task_id: str,
    task: str,
    system_prompt: str | None,
    graph: Any,
) -> None:
    """Execute the agent graph in the background."""
    try:
        await task_store.update_status(task_id, status="running")

        await task_store.update_progress(
            task_id,
            progress=0.0,
            agent="planner",
            message="Task started",
        )

        initial = _build_initial_state(
            task=task,
            system_prompt=system_prompt,
        )

        final_state: Any = await graph.ainvoke(initial)

        results, files = _state_to_results(final_state)

        result_dicts = [
            {
                "agent": r.agent,
                "success": r.success,
                "output": r.output,
                "message": r.message,
                "next_agent": r.next_agent,
                "metadata": r.metadata,
            }
            for r in results
        ]

        await task_store.set_result(
            task_id,
            results=result_dicts,
            files=files,
        )

        logger.info("Task %s completed successfully", task_id)

    except Exception as exc:
        logger.exception("Task %s failed", task_id)

        await task_store.set_error(
            task_id,
            error=str(exc),
        )


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=202,
    summary="Submit a new task",
)
async def create_task(
    request_body: CreateTaskRequest,
    request: Request,
    background_tasks: BackgroundTasks,
) -> TaskResponse:
    """
    Submit a task for execution.

    The task runs in the background. Use the returned task_id
    to poll status via GET /tasks/{task_id} or subscribe via WebSocket.
    """
    task_store = _get_task_store(request)

    record = await task_store.create(
        task=request_body.task,
        system_prompt=request_body.system_prompt,
        metadata=request_body.metadata,
    )

    graph: Any = getattr(request.app.state, "graph", None)

    if graph is not None:
        background_tasks.add_task(
            _run_task_background,
            task_store=task_store,
            task_id=record.task_id,
            task=request_body.task,
            system_prompt=request_body.system_prompt,
            graph=graph,
        )

    return TaskResponse(
        task_id=record.task_id,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get task status and results",
)
async def get_task(
    task_id: str,
    request: Request,
) -> TaskResponse:
    """
    Retrieve the current status and results of a task.
    """
    task_store = _get_task_store(request)

    record = await task_store.get(task_id)

    if record is None:
        raise TaskNotFoundError(task_id)

    results = [
        AgentResultResponse(
            agent=r.get("agent", ""),
            success=r.get("success", False),
            output=r.get("output"),
            message=r.get("message"),
            next_agent=r.get("next_agent"),
            metadata=r.get("metadata", {}),
        )
        for r in record.results
    ]

    return TaskResponse(
        task_id=record.task_id,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
        results=results,
        files=record.files,
        error=record.error,
    )


@router.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="List tasks",
)
async def list_tasks(
    request: Request,
    offset: int = 0,
    limit: int = 50,
    status: str | None = None,
) -> TaskListResponse:
    """
    List tasks with optional filtering and pagination.
    """
    task_store = _get_task_store(request)

    records, total = await task_store.list_tasks(
        offset=offset,
        limit=limit,
        status=status,
    )

    tasks = [
        TaskResponse(
            task_id=r.task_id,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
            error=r.error,
        )
        for r in records
    ]

    return TaskListResponse(
        tasks=tasks,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
)
async def delete_task(
    task_id: str,
    request: Request,
) -> None:
    """
    Delete a task and its results.
    """
    task_store = _get_task_store(request)

    deleted = await task_store.delete(task_id)

    if not deleted:
        raise TaskNotFoundError(task_id)
