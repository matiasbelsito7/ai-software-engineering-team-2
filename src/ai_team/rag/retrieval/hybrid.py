"""
Hybrid retriever.
"""

from __future__ import annotations

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import BaseRetriever


class HybridRetriever(BaseRetriever):
    """
    Combines multiple retrieval strategies.

    Example:

        Semantic
            +
        Keyword
            ↓
        Merge
            ↓
        Rerank
    """

    def __init__(
        self,
        *,
        semantic: BaseRetriever,
        keyword: BaseRetriever,
    ) -> None:
        self._semantic = semantic
        self._keyword = keyword

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Hybrid retrieval.

        Current implementation is intentionally left
        as a stub until score fusion is implemented.
        """

        raise NotImplementedError

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        """
        Build prompt context.
        """

        result = await self.search(
            query,
        )

        return RAGContext(
            chunks=[
                item.chunk
                for item in result.chunks
            ]
        )