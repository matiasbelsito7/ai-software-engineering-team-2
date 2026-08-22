"""
RAG tool.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult

if TYPE_CHECKING:
    from ai_team.rag.manager import RAGManager


class RAGTool(BaseTool):
    """
    Query the RAG (Retrieval-Augmented Generation) system.
    """

    def __init__(
        self,
        *,
        rag: RAGManager | None = None,
    ) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="rag",
                description="Query the RAG system for relevant documents.",
                category="information",
            )
        )
        self._rag = rag

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

        if self._rag is None:
            return ToolResult(
                success=True,
                output={
                    "query": query,
                    "results": [],
                    "message": "RAG system not available.",
                },
            )

        from ai_team.rag.models import RetrievalQuery

        retrieval_query = RetrievalQuery(query=query)
        result = await self._rag.search(retrieval_query)

        chunks = [
            {
                "content": rc.chunk.content,
                "uri": rc.chunk.uri,
                "score": rc.score,
            }
            for rc in result.chunks
        ]

        return ToolResult(
            success=True,
            output={
                "query": query,
                "results": chunks,
                "total": len(chunks),
            },
        )

    async def _index(self, params: dict[str, object]) -> ToolResult:
        path = str(params.get("path", ""))

        if not path:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        if self._rag is None:
            return ToolResult(
                success=True,
                output={
                    "path": path,
                    "message": "RAG system not available.",
                },
            )

        from pathlib import Path

        from ai_team.rag.loaders.repository import RepositoryLoader
        from ai_team.rag.models import DocumentSource
        from ai_team.shared.enums import SourceType

        target = Path(path)
        if not target.exists():
            return ToolResult(
                success=False,
                error=f"Path does not exist: {path}",
            )

        loader = RepositoryLoader()
        source = DocumentSource(uri=str(target), type=SourceType.FILE)
        document = await loader.load(source=source)

        await self._rag.index(document)

        return ToolResult(
            success=True,
            output={
                "path": path,
                "message": f"Indexed document from {path}.",
            },
        )

    async def _clear(self) -> ToolResult:
        if self._rag is not None:
            await self._rag.clear()

        return ToolResult(
            success=True,
            output={"message": "RAG store cleared."},
        )
