"""
Memory tool.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult

if TYPE_CHECKING:
    from ai_team.memory.manager import MemoryManager


class MemoryTool(BaseTool):
    """
    Query and manage agent memory.
    """

    def __init__(
        self,
        *,
        memory: MemoryManager | None = None,
    ) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="memory",
                description="Query and manage agent memory.",
                category="information",
            )
        )
        self._memory = memory

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

        if self._memory is None:
            return ToolResult(
                success=True,
                output={
                    "query": query,
                    "results": [],
                    "message": "Memory system not available.",
                },
            )

        from ai_team.memory.models import MemoryQuery

        memory_query = MemoryQuery(query=query)
        result = await self._memory.search(memory_query)

        entries = [
            {
                "content": e.content,
                "agent": e.agent.value if e.agent else None,
                "score": e.score,
            }
            for e in result.entries
        ]

        return ToolResult(
            success=True,
            output={
                "query": query,
                "results": entries,
                "total": len(entries),
            },
        )

    async def _add(self, params: dict[str, object]) -> ToolResult:
        content = str(params.get("content", ""))

        if not content:
            return ToolResult(
                success=False,
                error="Missing required parameter: content",
            )

        if self._memory is None:
            return ToolResult(
                success=True,
                output={
                    "content": content,
                    "message": "Memory system not available.",
                },
            )

        from ai_team.memory.models import MemoryEntry, MemoryMetadata
        from ai_team.shared.enums import MemoryType

        entry = MemoryEntry(
            memory_type=MemoryType.SHORT_TERM,
            content=content,
            metadata=MemoryMetadata(
                source="memory_tool",
                tags=["tool_input"],
            ),
        )

        await self._memory.add(entry)

        return ToolResult(
            success=True,
            output={
                "content": content,
                "message": "Memory entry stored.",
            },
        )

    async def _list(self) -> ToolResult:
        if self._memory is None:
            return ToolResult(
                success=True,
                output=[],
            )

        return ToolResult(
            success=True,
            output={"message": "Memory listing not supported. Use search instead."},
        )
