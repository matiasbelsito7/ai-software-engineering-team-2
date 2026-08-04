"""
Context-aware retriever.
"""

from __future__ import annotations

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import BaseRetriever


class ContextualRetriever(BaseRetriever):
    """
    Retrieval strategy that enriches a query with
    conversational or project context before searching.
    """

    def __init__(
        self,
        *,
        retriever: BaseRetriever,
    ) -> None:
        self._retriever = retriever

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Context-aware retrieval.

        Future implementation may:

            - rewrite the query
            - expand the query
            - inject project context
        """

        return await self._retriever.search(
            query,
        )

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        return await self._retriever.build_context(
            query,
        )