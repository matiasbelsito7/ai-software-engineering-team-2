"""
Unit tests for SSE streaming.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from ai_team.app.api.task_store import TaskStore


class TestStreamEvent:
    def test_stream_event_creation(self) -> None:
        from ai_team.app.api.schemas.tasks import StreamEvent

        event = StreamEvent(
            event="agent_progress",
            task_id="test-123",
            data={"agent": "backend", "progress": 0.5},
        )
        assert event.event == "agent_progress"
        assert event.task_id == "test-123"
        assert event.data["agent"] == "backend"
        assert event.timestamp is not None


class TestStreamHelpers:
    def test_format_sse(self) -> None:
        from ai_team.app.api.routers.streaming import _format_sse

        result = _format_sse("agent_progress", {"task_id": "123", "progress": 0.5})
        assert result.startswith("event: agent_progress\n")
        assert "data: " in result
        parsed = json.loads(result.split("data: ")[1].strip())
        assert parsed["task_id"] == "123"
        assert parsed["progress"] == 0.5


class TestStreamTaskEvents:
    @pytest.mark.asyncio
    async def test_stream_nonexistent_task(self) -> None:
        from ai_team.app.api.routers.streaming import _stream_task_events

        store = TaskStore()
        events = [event async for event in _stream_task_events(store, "nonexistent")]

        assert len(events) == 1
        assert "error" in events[0]

    @pytest.mark.asyncio
    async def test_stream_completed_task(self) -> None:
        from ai_team.app.api.routers.streaming import _stream_task_events

        store = TaskStore()
        record = await store.create(task="test task")
        await store.set_result(
            record.task_id,
            results=[{"agent": "planner", "success": True, "output": "done"}],
            files={},
        )

        events = [event async for event in _stream_task_events(store, record.task_id)]

        assert len(events) == 1
        data = json.loads(events[0].split("data: ")[1].strip())
        assert data["status"] == "completed"

    @pytest.mark.asyncio
    async def test_stream_failed_task(self) -> None:
        from ai_team.app.api.routers.streaming import _stream_task_events

        store = TaskStore()
        record = await store.create(task="test task")
        await store.set_error(record.task_id, error="Something went wrong")

        events = [event async for event in _stream_task_events(store, record.task_id)]

        assert len(events) == 1
        data = json.loads(events[0].split("data: ")[1].strip())
        assert "error" in data

    @pytest.mark.asyncio
    async def test_stream_progress_events(self) -> None:
        from ai_team.app.api.routers.streaming import _stream_task_events

        store = TaskStore()
        record = await store.create(task="test task")
        await store.update_status(record.task_id, status="running")

        async def _send_progress() -> None:
            await asyncio.sleep(0.1)
            await store.update_progress(
                record.task_id,
                progress=0.5,
                agent="backend",
                message="Working on it",
            )
            await asyncio.sleep(0.1)
            await store.set_result(
                record.task_id,
                results=[],
                files={},
            )

        events: list[str] = []

        async def _collect() -> None:
            async for event in _stream_task_events(store, record.task_id):
                events.extend([event])

        await asyncio.gather(_collect(), _send_progress())

        assert len(events) >= 2
        first_data = json.loads(events[0].split("data: ")[1].strip())
        assert first_data.get("status") == "running" or "task_id" in first_data
