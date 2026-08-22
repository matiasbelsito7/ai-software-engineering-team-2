"""
WebSocket router for real-time task progress.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

if TYPE_CHECKING:
    from ai_team.app.api.task_store import TaskStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


def _get_task_store_from_ws(websocket: WebSocket) -> TaskStore:
    return websocket.app.state.task_store  # type: ignore[no-any-return]


@router.websocket("/ws/tasks/{task_id}")
async def task_progress_ws(
    websocket: WebSocket,
    task_id: str,
) -> None:
    """
    WebSocket endpoint for real-time task progress updates.

    Connect to receive progress, completion, and error messages
    for a specific task.

    Messages are JSON-encoded with the following types:
    - progress: {type, task_id, status, agent, message, progress}
    - complete: {type, task_id, status, results, files}
    - error:    {type, task_id, error}
    """
    await websocket.accept()

    task_store = _get_task_store_from_ws(websocket)

    record = await task_store.get(task_id)

    if record is None:
        await websocket.send_json(
            {
                "type": "error",
                "task_id": task_id,
                "error": f"Task '{task_id}' not found.",
            }
        )
        await websocket.close(code=4004, reason="Task not found")
        return

    if record.status == "completed":
        await websocket.send_json(
            {
                "type": "complete",
                "task_id": task_id,
                "status": "completed",
                "results": record.results,
                "files": record.files,
            }
        )
        await websocket.close(code=1000, reason="Task already completed")
        return

    if record.status == "failed":
        await websocket.send_json(
            {
                "type": "error",
                "task_id": task_id,
                "error": record.error or "Task failed.",
            }
        )
        await websocket.close(code=1000, reason="Task already failed")
        return

    queue = task_store.subscribe(task_id)

    try:
        while True:
            try:
                message = await asyncio.wait_for(
                    queue.get(),
                    timeout=30.0,
                )
            except TimeoutError:
                await websocket.send_json({"type": "ping"})
                continue

            await websocket.send_json(message)

            msg_type = message.get("type")

            if msg_type in ("complete", "error"):
                break

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected from task %s", task_id)

    except Exception as exc:
        logger.exception("WebSocket error for task %s: %s", task_id, exc)

    finally:
        task_store.unsubscribe(task_id, queue)

        with contextlib.suppress(Exception):
            await websocket.close(code=1000)
