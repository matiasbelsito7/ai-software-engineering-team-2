"""
HTTP manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.tools.http.models import (
    DownloadResult,
    HttpResponse,
)

if TYPE_CHECKING:
    import httpx


class HttpManager:
    """
    Thin wrapper around httpx.AsyncClient.
    """

    def __init__(
        self,
        *,
        client: httpx.AsyncClient,
    ) -> None:

        self._client = client

    # ---------------------------------------------------------
    # HTTP METHODS
    # ---------------------------------------------------------

    async def get(
        self,
        *,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.get(
            url,
            params=params,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def post(
        self,
        *,
        url: str,
        json: dict[str, Any] | None = None,
        data: Any = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.post(
            url,
            json=json,
            data=data,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def put(
        self,
        *,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.put(
            url,
            json=json,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def patch(
        self,
        *,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.patch(
            url,
            json=json,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def delete(
        self,
        *,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.delete(
            url,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def head(
        self,
        *,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.head(
            url,
            headers=headers,
        )

        return self._response(
            response,
        )

    async def options(
        self,
        *,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:

        response = await self._client.options(
            url,
            headers=headers,
        )

        return self._response(
            response,
        )

    # ---------------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------------

    async def download(
        self,
        *,
        url: str,
    ) -> DownloadResult:

        response = await self._client.get(
            url,
        )

        response.raise_for_status()

        return DownloadResult(
            content=response.content,
            content_type=response.headers.get(
                "content-type",
            ),
            content_length=response.headers.get(
                "content-length",
            ),
        )

    # ---------------------------------------------------------
    # PRIVATE
    # ---------------------------------------------------------

    @staticmethod
    def _response(
        response: httpx.Response,
    ) -> HttpResponse:

        try:
            body = response.json()

        except Exception:
            body = response.text

        return HttpResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
        )
