"""
Integration tests for the FastAPI application.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from ai_team.app.api.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ================================================================
# Health
# ================================================================


@pytest.mark.asyncio
class TestHealthEndpoint:
    async def test_health(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "uptime_seconds" in data


# ================================================================
# Tasks - Create
# ================================================================


@pytest.mark.asyncio
class TestCreateTask:
    async def test_create_task_accepted(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/tasks",
            json={"task": "Build a REST API"},
        )
        assert response.status_code == 202
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "pending"
        assert "created_at" in data

    async def test_create_task_with_metadata(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/tasks",
            json={
                "task": "Build a REST API",
                "metadata": {"priority": "high"},
            },
        )
        assert response.status_code == 202

    async def test_create_task_empty_request(self, client: AsyncClient):
        response = await client.post("/api/v1/tasks", json={})
        assert response.status_code == 422

    async def test_create_task_invalid_body(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/tasks",
            json={"invalid_field": "value"},
        )
        assert response.status_code == 422

    async def test_create_task_empty_string(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/tasks",
            json={"task": ""},
        )
        assert response.status_code == 422


# ================================================================
# Tasks - Get
# ================================================================


@pytest.mark.asyncio
class TestGetTask:
    async def test_get_task_not_found(self, client: AsyncClient):
        response = await client.get("/api/v1/tasks/nonexistent-id")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    async def test_get_task_after_create(self, client: AsyncClient):
        create_resp = await client.post(
            "/api/v1/tasks",
            json={"task": "Test task"},
        )
        task_id = create_resp.json()["task_id"]

        get_resp = await client.get(f"/api/v1/tasks/{task_id}")
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["task_id"] == task_id
        assert data["status"] in ("pending", "running", "completed", "failed")


# ================================================================
# Tasks - List
# ================================================================


@pytest.mark.asyncio
class TestListTasks:
    async def test_list_tasks_empty(self, client: AsyncClient):
        response = await client.get("/api/v1/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert isinstance(data["tasks"], list)

    async def test_list_tasks_with_tasks(self, client: AsyncClient):
        await client.post(
            "/api/v1/tasks",
            json={"task": "Task 1"},
        )
        await client.post(
            "/api/v1/tasks",
            json={"task": "Task 2"},
        )

        response = await client.get("/api/v1/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2

    async def test_list_tasks_pagination(self, client: AsyncClient):
        response = await client.get("/api/v1/tasks?offset=0&limit=10")
        assert response.status_code == 200


# ================================================================
# Tasks - Delete
# ================================================================


@pytest.mark.asyncio
class TestDeleteTask:
    async def test_delete_task_not_found(self, client: AsyncClient):
        response = await client.delete("/api/v1/tasks/nonexistent-id")
        assert response.status_code == 404

    async def test_delete_task_success(self, client: AsyncClient):
        create_resp = await client.post(
            "/api/v1/tasks",
            json={"task": "To be deleted"},
        )
        task_id = create_resp.json()["task_id"]

        delete_resp = await client.delete(f"/api/v1/tasks/{task_id}")
        assert delete_resp.status_code == 204

        get_resp = await client.get(f"/api/v1/tasks/{task_id}")
        assert get_resp.status_code == 404
