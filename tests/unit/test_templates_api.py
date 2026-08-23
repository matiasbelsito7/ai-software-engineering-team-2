"""
API endpoint tests for templates.
"""

from __future__ import annotations

import asyncio

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


@pytest.mark.asyncio
class TestTemplatesAPI:
    async def test_list_templates(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/templates")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert "total" in data
        assert data["total"] > 0

    async def test_list_templates_by_category(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/templates?category=api")
        assert response.status_code == 200
        data = response.json()
        for template in data["templates"]:
            assert template["category"] == "api"

    async def test_list_templates_search(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/templates?search=crud")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    async def test_get_template(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/templates/crud_api")
        assert response.status_code == 200
        data = response.json()
        assert data["template_id"] == "crud_api"
        assert data["name"] == "CRUD REST API"

    async def test_get_template_not_found(self, client: AsyncClient) -> None:
        await asyncio.sleep(1.5)
        response = await client.get("/api/v1/templates/nonexistent")
        assert response.status_code == 404

    async def test_render_template(self, client: AsyncClient) -> None:
        await asyncio.sleep(1.5)
        response = await client.post(
            "/api/v1/templates/crud_api/render",
            json={"params": {"resource_name": "User", "fields": "name,email"}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["template_id"] == "crud_api"
        assert "User" in data["task"]

    async def test_render_template_invalid_params(self, client: AsyncClient) -> None:
        await asyncio.sleep(1.5)
        response = await client.post(
            "/api/v1/templates/crud_api/render",
            json={"params": {}},
        )
        assert response.status_code == 422

    async def test_render_template_not_found(self, client: AsyncClient) -> None:
        await asyncio.sleep(1.5)
        response = await client.post(
            "/api/v1/templates/nonexistent/render",
            json={"params": {}},
        )
        assert response.status_code == 404

    async def test_create_task_from_template(self, client: AsyncClient) -> None:
        await asyncio.sleep(1.5)
        response = await client.post(
            "/api/v1/templates/crud_api/create-task",
            json={"params": {"resource_name": "Product", "fields": "name,price"}},
        )
        assert response.status_code == 202
        data = response.json()
        assert data["template_id"] == "crud_api"
        assert "Product" in data["task"]
