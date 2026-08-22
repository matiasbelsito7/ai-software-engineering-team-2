"""
Unit tests for security middleware and audit logging.
"""

from __future__ import annotations

import time

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from ai_team.app.api.main import app
from ai_team.app.api.middleware.auth import APIKeyAuthMiddleware
from ai_team.app.api.middleware.rate_limit import _TokenBucket
from ai_team.app.api.security.audit import SecurityAuditLogger, SecurityEvent


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# =====================================================================
# Token Bucket
# =====================================================================


class TestTokenBucket:
    def test_consume_within_capacity(self) -> None:
        bucket = _TokenBucket(capacity=5, refill_rate=1.0)
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is True

    def test_consume_exceeds_capacity(self) -> None:
        bucket = _TokenBucket(capacity=2, refill_rate=0.0)
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is False

    def test_refill(self) -> None:
        bucket = _TokenBucket(capacity=2, refill_rate=100.0)
        assert bucket.consume() is True
        assert bucket.consume() is True
        assert bucket.consume() is False
        time.sleep(0.05)
        assert bucket.consume() is True

    def test_retry_after(self) -> None:
        bucket = _TokenBucket(capacity=1, refill_rate=10.0)
        assert bucket.consume() is True
        assert bucket.retry_after > 0.0


# =====================================================================
# Security Audit Logger
# =====================================================================


class TestSecurityAuditLogger:
    def test_auth_success(self) -> None:
        logger = SecurityAuditLogger()
        logger.auth_success(path="/api/v1/tasks", ip="127.0.0.1", api_key_suffix="abcd")

    def test_auth_fail_missing(self) -> None:
        logger = SecurityAuditLogger()
        logger.auth_fail_missing(path="/api/v1/tasks", ip="127.0.0.1")

    def test_auth_fail_invalid(self) -> None:
        logger = SecurityAuditLogger()
        logger.auth_fail_invalid(path="/api/v1/tasks", ip="127.0.0.1", api_key_suffix="wxyz")

    def test_rate_limit_ip(self) -> None:
        logger = SecurityAuditLogger()
        logger.rate_limit(path="/api/v1/tasks", ip="127.0.0.1", limit_type="ip")

    def test_rate_limit_key(self) -> None:
        logger = SecurityAuditLogger()
        logger.rate_limit(path="/api/v1/tasks", api_key_suffix="test", limit_type="key")

    def test_suspicious_input(self) -> None:
        logger = SecurityAuditLogger()
        logger.suspicious_input(path="/api/v1/tasks", ip="127.0.0.1", detail="injection detected")

    def test_log_event(self) -> None:
        logger = SecurityAuditLogger()
        logger.log_event(
            event=SecurityEvent.AUTH_SUCCESS,
            path="/test",
            ip="1.2.3.4",
            api_key_suffix="abcd",
            detail="test event",
        )


# =====================================================================
# Security Headers (via HTTP client)
# =====================================================================


@pytest.mark.asyncio
class TestSecurityHeaders:
    async def test_security_headers_present(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        assert "strict-transport-security" in response.headers
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "content-security-policy" in response.headers
        assert "referrer-policy" in response.headers
        assert "permissions-policy" in response.headers
        assert "cache-control" in response.headers

    async def test_x_content_type_options(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/health")
        assert response.headers["x-content-type-options"] == "nosniff"

    async def test_x_frame_options(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/health")
        assert response.headers["x-frame-options"] == "DENY"

    async def test_request_id_generated(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/health")
        assert "x-request-id" in response.headers
        assert len(response.headers["x-request-id"]) > 0

    async def test_request_id_preserved(self, client: AsyncClient) -> None:
        response = await client.get(
            "/api/v1/health",
            headers={"X-Request-Id": "test-id-123"},
        )
        assert response.headers.get("x-request-id") == "test-id-123"


# =====================================================================
# Rate Limiting
# =====================================================================


@pytest.mark.asyncio
class TestRateLimiting:
    async def test_health_bypasses_rate_limit(self, client: AsyncClient) -> None:
        for _ in range(50):
            response = await client.get("/api/v1/health")
            assert response.status_code == 200


# =====================================================================
# Auth Middleware (unit test with standalone Starlette app)
# =====================================================================


class TestAPIKeyAuthMiddleware:
    def _build_app(self, api_keys: list[str]) -> Starlette:
        async def dummy(request):  # type: ignore[no-untyped-def]
            return PlainTextResponse("ok")

        test_app = Starlette()
        test_app.add_middleware(
            APIKeyAuthMiddleware,
            api_keys=api_keys,
        )
        test_app.add_route("/test", dummy)
        return test_app

    def test_missing_key_returns_401(self) -> None:
        test_app = self._build_app(["valid-key-123"])
        client_test = TestClient(test_app)
        response = client_test.get("/test")
        assert response.status_code == 401
        assert "Missing API key" in response.json()["detail"]

    def test_invalid_key_returns_401(self) -> None:
        test_app = self._build_app(["valid-key-123"])
        client_test = TestClient(test_app)
        response = client_test.get("/test", headers={"X-API-Key": "wrong-key"})
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]

    def test_valid_key_passes(self) -> None:
        test_app = self._build_app(["valid-key-123"])
        client_test = TestClient(test_app)
        response = client_test.get("/test", headers={"X-API-Key": "valid-key-123"})
        assert response.status_code == 200
        assert response.text == "ok"

    def test_open_endpoint_bypasses_auth(self) -> None:
        async def health(request):  # type: ignore[no-untyped-def]
            return PlainTextResponse("ok")

        test_app = Starlette()
        test_app.add_middleware(
            APIKeyAuthMiddleware,
            api_keys=["valid-key"],
        )
        test_app.add_route("/api/v1/health", health)
        client_test = TestClient(test_app)
        response = client_test.get("/api/v1/health")
        assert response.status_code == 200
