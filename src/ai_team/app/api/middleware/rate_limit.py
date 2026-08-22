"""
Rate limiting middleware using token bucket algorithm.
"""

from __future__ import annotations

import logging
import time
from threading import Lock
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request  # noqa: TC002
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class _TokenBucket:
    """Thread-safe token bucket for rate limiting."""

    __slots__ = ("capacity", "last_refill", "refill_rate", "tokens")

    def __init__(self, capacity: int, refill_rate: float) -> None:
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()

    def consume(self) -> bool:
        now = time.monotonic()

        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate,
        )
        self.last_refill = now

        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True

        return False

    @property
    def retry_after(self) -> float:
        if self.tokens >= 1.0:
            return 0.0

        return max(0.0, (1.0 - self.tokens) / self.refill_rate)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Per-IP and per-API-key rate limiting.

    Uses a token bucket algorithm with configurable capacity
    and refill rate. Rate limits are tracked separately for
    IP addresses and API keys.
    """

    def __init__(
        self,
        app: Any,
        *,
        per_ip: int = 100,
        per_key: int = 200,
        burst: int = 20,
        audit_logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(app)

        self._per_ip = per_ip
        self._per_key = per_key
        self._burst = burst

        self._ip_buckets: dict[str, _TokenBucket] = {}
        self._key_buckets: dict[str, _TokenBucket] = {}
        self._lock = Lock()
        self._audit = audit_logger or logging.getLogger(__name__)

    def _get_ip_bucket(self, ip: str) -> _TokenBucket:
        with self._lock:
            if ip not in self._ip_buckets:
                self._ip_buckets[ip] = _TokenBucket(
                    capacity=self._burst,
                    refill_rate=self._per_ip / 60.0,
                )
            return self._ip_buckets[ip]

    def _get_key_bucket(self, key: str) -> _TokenBucket:
        with self._lock:
            if key not in self._key_buckets:
                self._key_buckets[key] = _TokenBucket(
                    capacity=self._burst,
                    refill_rate=self._per_key / 60.0,
                )
            return self._key_buckets[key]

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        path = request.url.path

        if path in ("/api/v1/health", "/docs", "/redoc", "/openapi.json"):
            response: Response = await call_next(request)
            return response

        if path.startswith("/docs") or path.startswith("/redoc"):
            response = await call_next(request)
            return response

        if path.startswith("/openapi"):
            response = await call_next(request)
            return response

        client_ip = request.client.host if request.client else "unknown"

        ip_bucket = self._get_ip_bucket(client_ip)

        if not ip_bucket.consume():
            retry = int(ip_bucket.retry_after) + 1

            self._audit.warning(
                "RATE_LIMIT ip=%s path=%s retry_after=%d",
                client_ip,
                path,
                retry,
            )

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Try again later.",
                    "error_code": "rate_limit_exceeded",
                    "retry_after": retry,
                },
                headers={"Retry-After": str(retry)},
            )

        api_key = request.headers.get("x-api-key")

        if api_key:
            key_bucket = self._get_key_bucket(api_key)

            if not key_bucket.consume():
                retry = int(key_bucket.retry_after) + 1

                self._audit.warning(
                    "RATE_LIMIT key=***%s path=%s retry_after=%d",
                    api_key[-4:] if len(api_key) >= 4 else "****",
                    path,
                    retry,
                )

                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded. Try again later.",
                        "error_code": "rate_limit_exceeded",
                        "retry_after": retry,
                    },
                    headers={"Retry-After": str(retry)},
                )

        response = await call_next(request)

        remaining_ip = max(0, int(ip_bucket.tokens))
        response.headers["X-RateLimit-Limit"] = str(self._per_ip)
        response.headers["X-RateLimit-Remaining"] = str(remaining_ip)

        return response
