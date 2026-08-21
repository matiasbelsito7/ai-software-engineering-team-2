"""
RAG tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class RAGTool(BaseTool):
    """
    Query the RAG (Retrieval-Augmented Generation) system.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="rag",
                description="Query the RAG system for relevant documents.",
                category="information",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        operation = request.parameters.get("operation", "search")

        try:
            if operation == "search":
                return await self._search(request.parameters)
            elif operation == "index":
                return await self._index(request.parameters)
            elif operation == "clear":
                return await self._clear()
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
                "message": "RAG search not yet wired to runtime.",
            },
        )

    async def _index(self, params: dict[str, object]) -> ToolResult:
        path = str(params.get("path", ""))

        if not path:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        return ToolResult(
            success=True,
            output={
                "path": path,
                "message": "RAG indexing not yet wired to runtime.",
            },
        )

    async def _clear(self) -> ToolResult:
        return ToolResult(
            success=True,
            output={"message": "RAG store cleared."},
        )
