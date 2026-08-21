"""
Hybrid retriever.
"""

from __future__ import annotations

import logging

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
)
from ai_team.rag.retrieval.base import BaseRetriever

logger = logging.getLogger(__name__)


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
        try:
            semantic_result = await self._semantic.search(query)
        except Exception:
            logger.debug("Semantic search failed, falling back to keyword")
            return await self._keyword.search(query)

        try:
            keyword_result = await self._keyword.search(query)
        except Exception:
            return semantic_result

        seen: set[str] = set()
        merged: list[RetrievedChunk] = []
        for item in semantic_result.chunks:
            if str(item.chunk.id) not in seen:
                seen.add(str(item.chunk.id))
                merged.append(item)
        for item in keyword_result.chunks:
            if str(item.chunk.id) not in seen:
                seen.add(str(item.chunk.id))
                merged.append(item)

        return RetrievalResult(query=query, chunks=merged)

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        result = await self.search(query)

        return RAGContext(
            chunks=[
                item.chunk
                for item in result.chunks
            ]
        )
