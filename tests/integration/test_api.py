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


# ================================================================
# Tasks
# ================================================================


@pytest.mark.asyncio
class TestTaskEndpoint:
    async def test_get_task_not_implemented(self, client: AsyncClient):
        response = await client.get("/api/v1/tasks/some-id")
        assert response.status_code == 501

    async def test_post_task_empty_request(self, client: AsyncClient):
        response = await client.post("/api/v1/tasks", json={})
        assert response.status_code == 422

    async def test_post_task_invalid_body(self, client: AsyncClient):
        response = await client.post("/api/v1/tasks", json={"invalid_field": "value"})
        assert response.status_code == 422
