"""
In-memory task store for tracking task lifecycle.

Provides thread-safe storage for tasks with status tracking,
result persistence, and progress updates. Can be swapped for
a Redis or database-backed store later.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class TaskRecord:
    """A single task record held in the store."""

    __slots__ = (
        "created_at",
        "current_agent",
        "error",
        "files",
        "metadata",
        "progress",
        "results",
        "status",
        "system_prompt",
        "task",
        "task_id",
        "updated_at",
    )

    def __init__(
        self,
        *,
        task_id: str | None = None,
        task: str,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        now = datetime.now(UTC).isoformat()

        self.task_id: str = task_id or str(uuid4())
        self.task: str = task
        self.system_prompt: str | None = system_prompt
        self.metadata: dict[str, Any] = metadata or {}
        self.status: str = "pending"
        self.results: list[dict[str, Any]] = []
        self.files: dict[str, str] = {}
        self.error: str | None = None
        self.created_at: str = now
        self.updated_at: str = now
        self.progress: float = 0.0
        self.current_agent: str | None = None

    def mark_running(self, *, agent: str | None = None) -> None:
        self.status = "running"
        self.current_agent = agent
        self.updated_at = datetime.now(UTC).isoformat()

    def mark_completed(
        self,
        *,
        results: list[dict[str, Any]] | None = None,
        files: dict[str, str] | None = None,
    ) -> None:
        self.status = "completed"
        if results is not None:
            self.results = results
        if files is not None:
            self.files = files
        self.progress = 1.0
        self.updated_at = datetime.now(UTC).isoformat()

    def mark_failed(self, *, error: str) -> None:
        self.status = "failed"
        self.error = error
        self.updated_at = datetime.now(UTC).isoformat()

    def update_progress(
        self,
        *,
        progress: float,
        agent: str | None = None,
        message: str | None = None,
    ) -> None:
        self.progress = min(max(progress, 0.0), 1.0)
        if agent is not None:
            self.current_agent = agent
        self.updated_at = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task": self.task,
            "system_prompt": self.system_prompt,
            "metadata": self.metadata,
            "status": self.status,
            "results": self.results,
            "files": self.files,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "progress": self.progress,
            "current_agent": self.current_agent,
        }


class TaskStore:
    """
    In-memory task store with async-safe access.

    Uses an asyncio Lock to protect concurrent mutations.
    """

    def __init__(self) -> None:
        self._tasks: dict[str, TaskRecord] = {}
        self._lock: asyncio.Lock = asyncio.Lock()
        self._subscribers: dict[str, list[asyncio.Queue[Any]]] = {}
        self._pending_approvals: dict[str, dict[str, dict[str, Any]]] = {}
        self._approval_events: dict[str, asyncio.Event] = {}

    async def create(
        self,
        *,
        task: str,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
        task_id: str | None = None,
    ) -> TaskRecord:
        record = TaskRecord(
            task_id=task_id,
            task=task,
            system_prompt=system_prompt,
            metadata=metadata,
        )

        async with self._lock:
            self._tasks[record.task_id] = record

        logger.info("Task created: %s", record.task_id)

        return record

    async def get(self, task_id: str) -> TaskRecord | None:
        async with self._lock:
            return self._tasks.get(task_id)

    async def list_tasks(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> tuple[list[TaskRecord], int]:
        async with self._lock:
            records = list(self._tasks.values())

        if status is not None:
            records = [r for r in records if r.status == status]

        total = len(records)

        records.sort(key=lambda r: r.created_at, reverse=True)

        return records[offset : offset + limit], total

    async def update_status(
        self,
        task_id: str,
        *,
        status: str,
    ) -> TaskRecord | None:
        async with self._lock:
            record = self._tasks.get(task_id)
            if record is None:
                return None

            record.status = status
            record.updated_at = datetime.now(UTC).isoformat()

        return record

    async def set_result(
        self,
        task_id: str,
        *,
        results: list[dict[str, Any]],
        files: dict[str, str] | None = None,
    ) -> TaskRecord | None:
        async with self._lock:
            record = self._tasks.get(task_id)
            if record is None:
                return None

            record.mark_completed(results=results, files=files)

        await self._notify(
            task_id,
            {
                "type": "complete",
                "task_id": task_id,
                "status": "completed",
                "results": results,
                "files": files or {},
            },
        )

        return record

    async def set_error(
        self,
        task_id: str,
        *,
        error: str,
    ) -> TaskRecord | None:
        async with self._lock:
            record = self._tasks.get(task_id)
            if record is None:
                return None

            record.mark_failed(error=error)

        await self._notify(
            task_id,
            {
                "type": "error",
                "task_id": task_id,
                "error": error,
            },
        )

        return record

    async def update_progress(
        self,
        task_id: str,
        *,
        progress: float,
        agent: str | None = None,
        message: str | None = None,
    ) -> TaskRecord | None:
        async with self._lock:
            record = self._tasks.get(task_id)
            if record is None:
                return None

            record.update_progress(
                progress=progress,
                agent=agent,
                message=message,
            )

        await self._notify(
            task_id,
            {
                "type": "progress",
                "task_id": task_id,
                "status": "running",
                "agent": agent,
                "message": message,
                "progress": progress,
            },
        )

        return record

    async def delete(self, task_id: str) -> bool:
        async with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True

        return False

    def subscribe(self, task_id: str) -> asyncio.Queue[Any]:
        queue: asyncio.Queue[Any] = asyncio.Queue()

        if task_id not in self._subscribers:
            self._subscribers[task_id] = []

        self._subscribers[task_id].append(queue)

        return queue

    def unsubscribe(self, task_id: str, queue: asyncio.Queue[Any]) -> None:
        if task_id in self._subscribers:
            self._subscribers[task_id] = [q for q in self._subscribers[task_id] if q is not queue]

    async def _notify(self, task_id: str, message: dict[str, Any]) -> None:
        subscribers = self._subscribers.get(task_id, [])

        for queue in subscribers:
            try:
                queue.put_nowait(message)
            except asyncio.QueueFull:
                logger.warning(
                    "Subscriber queue full for task %s, dropping message",
                    task_id,
                )

    # ------------------------------------------------------------------
    # Approval (human-in-the-loop)
    # ------------------------------------------------------------------

    async def request_approval(
        self,
        task_id: str,
        *,
        approval_id: str,
        command: str,
        agent: str | None = None,
        description: str | None = None,
    ) -> None:
        """Store a pending approval and notify subscribers."""

        approval_record = {
            "approval_id": approval_id,
            "task_id": task_id,
            "command": command,
            "agent": agent,
            "description": description,
            "status": "pending",
        }

        async with self._lock:
            if task_id not in self._pending_approvals:
                self._pending_approvals[task_id] = {}

            self._pending_approvals[task_id][approval_id] = approval_record

            event = asyncio.Event()
            self._approval_events[approval_id] = event

        await self._notify(
            task_id,
            {
                "type": "approval_request",
                "task_id": task_id,
                "approval_id": approval_id,
                "command": command,
                "agent": agent,
                "description": description,
            },
        )

    async def wait_approval(
        self,
        approval_id: str,
        *,
        timeout: float = 300.0,
    ) -> bool:
        """Block until the approval is resolved or timeout."""

        event = self._approval_events.get(approval_id)

        if event is None:
            return False

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
        except TimeoutError:
            return False

        return True

    async def resolve_approval(
        self,
        task_id: str,
        *,
        approval_id: str,
        approved: bool,
    ) -> dict[str, Any] | None:
        """Resolve a pending approval and notify subscribers."""

        async with self._lock:
            task_approvals = self._pending_approvals.get(task_id, {})
            record = task_approvals.pop(approval_id, None)

            event = self._approval_events.pop(approval_id, None)

        if record is None:
            return None

        record["status"] = "approved" if approved else "rejected"

        if event is not None:
            event.set()

        await self._notify(
            task_id,
            {
                "type": "approval_response",
                "task_id": task_id,
                "approval_id": approval_id,
                "approved": approved,
                "command": record["command"],
            },
        )

        return record

    async def get_pending_approvals(
        self,
        task_id: str,
    ) -> list[dict[str, Any]]:
        """Return all pending approvals for a task."""

        async with self._lock:
            task_approvals = self._pending_approvals.get(task_id, {})
            return list(task_approvals.values())
