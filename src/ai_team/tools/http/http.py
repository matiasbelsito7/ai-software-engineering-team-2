"""
HTTP tool.
"""

from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable

from ai_team.tools.base import BaseTool
from ai_team.tools.http.manager import HttpManager
from ai_team.tools.http.policy import HttpPolicy
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)


class HttpTool(BaseTool):
    """
    HTTP operations.
    """

    def __init__(
        self,
        *,
        manager: HttpManager,
        policy: HttpPolicy,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="http",
                description="Execute HTTP requests.",
                category="network",
            ),
        )

        self._manager = manager
        self._policy = policy

        self._operations: dict[
            str,
            Callable[
                [dict],
                Awaitable[ToolResult],
            ],
        ] = {

            "get": self._get,

            "post": self._post,

            "put": self._put,

            "patch": self._patch,

            "delete": self._delete,

            "head": self._head,

            "options": self._options,

            "download": self._download,
        }

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get(
            "operation",
        )

        self._policy.validate_operation(
            operation,
        )

        handler = self._operations.get(
            operation,
        )

        if handler is None:

            return ToolResult(
                success=False,
                error=f"Unknown HTTP operation '{operation}'.",
            )

        try:

            return await handler(
                request.parameters,
            )

        except Exception as exc:

            return ToolResult(
                success=False,
                error=str(exc),
            )

    # ---------------------------------------------------------

    def _validate_request(
        self,
        parameters: dict,
    ) -> None:

        self._policy.validate_url(
            parameters["url"],
        )

        self._policy.validate_headers(
            parameters.get("headers"),
        )

        self._policy.validate_payload(
            parameters.get("json"),
        )

    # ---------------------------------------------------------

    async def _get(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.get(
            url=parameters["url"],
            params=parameters.get("params"),
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _post(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.post(
            url=parameters["url"],
            json=parameters.get("json"),
            data=parameters.get("data"),
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _put(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.put(
            url=parameters["url"],
            json=parameters.get("json"),
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _patch(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.patch(
            url=parameters["url"],
            json=parameters.get("json"),
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _delete(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.delete(
            url=parameters["url"],
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _head(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.head(
            url=parameters["url"],
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _options(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._validate_request(parameters)

        response = await self._manager.options(
            url=parameters["url"],
            headers=parameters.get("headers"),
        )

        return ToolResult(
            success=True,
            output=response,
        )

    async def _download(
        self,
        parameters: dict,
    ) -> ToolResult:

        self._policy.validate_url(
            parameters["url"],
        )

        result = await self._manager.download(
            url=parameters["url"],
        )

        return ToolResult(
            success=True,
            output=result,
        )