"""
Memory tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class MemoryTool(BaseTool):
    """
    Query and manage agent memory.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="memory",
                description="Query and manage agent memory.",
                category="information",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        operation = request.parameters.get("operation", "search")

        try:
            if operation == "search":
                return await self._search(request.parameters)
            elif operation == "add":
                return await self._add(request.parameters)
            elif operation == "list":
                return await self._list()
            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported operation: {operation}",
                )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

    async def _search(self, params: dict[str, object]) -> ToolResult:
        query = str(params.get("query", ""))

        if not query:
            return ToolResult(
                success=False,
                error="Missing required parameter: query",
            )

        return ToolResult(
            success=True,
            output={
                "query": query,
                "results": [],
                "message": "Memory search not yet wired to runtime.",
            },
        )

    async def _add(self, params: dict[str, object]) -> ToolResult:
        content = str(params.get("content", ""))

        if not content:
            return ToolResult(
                success=False,
                error="Missing required parameter: content",
            )

        return ToolResult(
            success=True,
            output={
                "content": content,
                "message": "Memory entry stored.",
            },
        )

    async def _list(self) -> ToolResult:
        return ToolResult(
            success=True,
            output=[],
        )
