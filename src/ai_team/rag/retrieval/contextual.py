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

    Appends context keywords to broaden recall.
    """

    def __init__(
        self,
        *,
        retriever: BaseRetriever,
        context_prefix: str = "",
    ) -> None:
        self._retriever = retriever
        self._context_prefix = context_prefix

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        enriched_query = self._rewrite_query(query)

        return await self._retriever.search(enriched_query)

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        enriched_query = self._rewrite_query(query)

        return await self._retriever.build_context(enriched_query)

    def _rewrite_query(
        self,
        query: RetrievalQuery,
    ) -> RetrievalQuery:
        if self._context_prefix:
            return RetrievalQuery(
                query=f"{self._context_prefix} {query.query}",
                top_k=query.top_k,
            )

        return query
