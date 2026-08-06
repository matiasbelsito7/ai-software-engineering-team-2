"""
Browser tool.
"""

from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable

from ai_team.tools.base import BaseTool
from ai_team.tools.browser.manager import BrowserManager
from ai_team.tools.browser.models import BrowserSession
from ai_team.tools.browser.policy import BrowserPolicy
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)


class BrowserTool(BaseTool):
    """
    Browser operations.
    """

    def __init__(
        self,
        *,
        manager: BrowserManager,
        policy: BrowserPolicy,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="browser",
                description="Interact with web pages.",
                category="browser",
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

            "goto": self._goto,

            "content": self._content,

            "title": self._title,

            "click": self._click,

            "fill": self._fill,

            "evaluate": self._evaluate,

            "screenshot": self._screenshot,

            "close": self._close,
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
                error=f"Unknown browser operation '{operation}'.",
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

    async def _goto(
        self,
        parameters: dict,
    ) -> ToolResult:

        url = parameters["url"]

        self._policy.validate_url(
            url,
        )

        session = await self._manager.goto(
            url,
        )

        return ToolResult(
            success=True,
            output=session,
        )

    async def _content(
        self,
        parameters: dict,
    ) -> ToolResult:

        content = await self._manager.content(
            parameters["session"],
        )

        return ToolResult(
            success=True,
            output=content,
        )

    async def _title(
        self,
        parameters: dict,
    ) -> ToolResult:

        title = await self._manager.title(
            parameters["session"],
        )

        return ToolResult(
            success=True,
            output=title,
        )

    async def _click(
        self,
        parameters: dict,
    ) -> ToolResult:

        selector = parameters["selector"]

        self._policy.validate_selector(
            selector,
        )

        await self._manager.click(
            parameters["session"],
            selector,
        )

        return ToolResult(
            success=True,
        )

    async def _fill(
        self,
        parameters: dict,
    ) -> ToolResult:

        selector = parameters["selector"]

        self._policy.validate_selector(
            selector,
        )

        await self._manager.fill(
            parameters["session"],
            selector,
            parameters["value"],
        )

        return ToolResult(
            success=True,
        )

    async def _evaluate(
        self,
        parameters: dict,
    ) -> ToolResult:

        javascript = parameters["javascript"]

        self._policy.validate_script(
            javascript,
        )

        result = await self._manager.evaluate(
            parameters["session"],
            javascript,
        )

        return ToolResult(
            success=True,
            output=result,
        )

    async def _screenshot(
        self,
        parameters: dict,
    ) -> ToolResult:

        await self._manager.screenshot(
            parameters["session"],
            parameters["path"],
        )

        return ToolResult(
            success=True,
        )

    async def _close(
        self,
        parameters: dict,
    ) -> ToolResult:

        await self._manager.close(
            parameters["session"],
        )

        return ToolResult(
            success=True,
        )