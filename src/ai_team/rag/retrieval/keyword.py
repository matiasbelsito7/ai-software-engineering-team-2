"""
Keyword retriever.
"""

from __future__ import annotations

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import BaseRetriever


class KeywordRetriever(BaseRetriever):
    """
    Keyword-based retrieval.

    Future implementation:
        BM25
        TF-IDF
    """

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        return RetrievalResult(query=query, chunks=[])

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        return RAGContext(chunks=[], summary=None)
