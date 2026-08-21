"""
Central tool executor.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.observability.manager import ObservationManager
    from ai_team.tools.manager import ToolManager
    from ai_team.tools.models import (
        ToolRequest,
        ToolResult,
    )


class ToolExecutor:
    """
    Central entry point for every tool execution.

    All agents must execute tools through this class.
    """

    def __init__(
        self,
        *,
        manager: ToolManager,
        observations: ObservationManager | None = None,
    ) -> None:

        self._manager = manager
        self._observations = observations

    # ---------------------------------------------------------

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        tool = self._manager.get(
            request.tool,
        )

        started = time.perf_counter()

        success = False

        try:
            result = await tool.run(
                request,
            )

            success = result.success

            return result

        finally:
            if self._observations is not None:
                await self._observations.record_tool_call(
                    execution_id="",
                    agent="",
                    tool=request.tool,
                    latency_ms=(time.perf_counter() - started),
                    success=success,
                )

    # ---------------------------------------------------------

    def has_tool(
        self,
        tool_name: str,
    ) -> bool:

        return self._manager.has(
            tool_name,
        )

    def available_tools(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._manager.names(),
        )
