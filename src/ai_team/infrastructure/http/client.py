"""
Shared HTTP client for the entire application.

This module centralizes every HTTP configuration used across
the project, ensuring that all external services share the
same networking policies.

Used by:

- OpenRouter
- Ollama
- Qdrant
- GitHub
- Docker
- External APIs
"""

from __future__ import annotations

from typing import Any

import httpx

from ai_team.infrastructure.config.settings import settings


DEFAULT_LIMITS = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
)

DEFAULT_TIMEOUT = httpx.Timeout(
    connect=settings.http.connect_timeout,
    read=settings.http.read_timeout,
    write=settings.http.write_timeout,
    pool=settings.http.pool_timeout,
)


class HTTPClient:
    """
    Shared HTTP client factory.

    This class is intentionally stateless.
    """

    @staticmethod
    def create(
        *,
        base_url: str | None = None,
        headers: dict[str, str] | None = None,
        timeout: httpx.Timeout | None = None,
    ) -> httpx.AsyncClient:
        """
        Create a configured AsyncClient.
        """

        return httpx.AsyncClient(
            base_url=base_url or "",
            headers=headers,
            timeout=timeout or DEFAULT_TIMEOUT,
            limits=DEFAULT_LIMITS,
            follow_redirects=True,
            http2=True,
        )

    @staticmethod
    async def close(client: httpx.AsyncClient) -> None:
        """
        Close an AsyncClient.
        """

        await client.aclose()