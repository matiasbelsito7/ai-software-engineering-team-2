"""
SSE streaming endpoint for real-time task progress.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ai_team.app.api.task_store import TaskStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["streaming"])


def _get_task_store(request: Request) -> TaskStore:
    return request.app.state.task_store  # type: ignore[no-any-return]


def _format_sse(event: str, data: dict[str, Any]) -> str:
    """Format a dict as an SSE message."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def _stream_task_events(
    task_store: TaskStore,
    task_id: str,
) -> AsyncIterator[str]:
    """Stream task events as SSE."""
    record = await task_store.get(task_id)

    if record is None:
        yield _format_sse(
            "error",
            {"task_id": task_id, "error": f"Task '{task_id}' not found"},
        )
        return

    if record.status == "completed":
        yield _format_sse(
            "task_complete",
            {
                "task_id": task_id,
                "status": "completed",
                "results": record.results,
                "files": record.files,
            },
        )
        return

    if record.status == "failed":
        yield _format_sse(
            "error",
            {"task_id": task_id, "error": record.error or "Task failed"},
        )
        return

    # Send initial state
    yield _format_sse(
        "task_start",
        {
            "task_id": task_id,
            "status": record.status,
            "progress": record.progress,
        },
    )

    queue = task_store.subscribe(task_id)
    try:
        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=30.0)
            except TimeoutError:
                yield _format_sse("ping", {"task_id": task_id})
                continue

            event_type = message.get("type", "progress")

            if event_type == "progress":
                yield _format_sse(
                    "agent_progress",
                    {
                        "task_id": task_id,
                        "status": message.get("status", "running"),
                        "agent": message.get("agent"),
                        "message": message.get("message"),
                        "progress": message.get("progress", 0.0),
                    },
                )
            elif event_type == "complete":
                yield _format_sse(
                    "task_complete",
                    {
                        "task_id": task_id,
                        "status": "completed",
                        "results": message.get("results", []),
                        "files": message.get("files", {}),
                    },
                )
                break
            elif event_type == "error":
                yield _format_sse(
                    "error",
                    {
                        "task_id": task_id,
                        "error": message.get("error", "Unknown error"),
                    },
                )
                break
    except asyncio.CancelledError:
        logger.info("SSE stream cancelled for task %s", task_id)
    except Exception as exc:
        logger.exception("SSE stream error for task %s: %s", task_id, exc)
        yield _format_sse(
            "error",
            {"task_id": task_id, "error": str(exc)},
        )
    finally:
        task_store.unsubscribe(task_id, queue)


@router.get(
    "/tasks/{task_id}/stream",
    summary="Stream task progress via SSE",
)
async def stream_task(
    task_id: str,
    request: Request,
) -> AsyncIterator[str]:
    """
    Stream real-time task progress via Server-Sent Events.

    Events:
    - task_start: Task execution started
    - agent_progress: Agent is working (progress 0.0-1.0)
    - agent_complete: Agent finished
    - task_complete: Task finished with results
    - error: Task failed
    - ping: Keepalive (every 30s)
    """
    task_store = _get_task_store(request)

    async for event in _stream_task_events(task_store, task_id):
        if await request.is_disconnected():
            break
        yield event
