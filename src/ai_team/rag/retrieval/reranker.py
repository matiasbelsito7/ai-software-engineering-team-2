"""
Retriever wrapper that reranks retrieved chunks.
"""

from __future__ import annotations

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import BaseRetriever


class RerankerRetriever(BaseRetriever):
    """
    Applies reranking on top of another retriever.

    Future implementations may use:

        - CrossEncoder
        - BGE Reranker
        - LLM-as-a-Reranker
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
        Retrieve documents and rerank them.
        """

        result = await self._retriever.search(
            query,
        )

        #
        # Future reranking logic.
        #

        return result

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        result = await self.search(
            query,
        )

        return RAGContext(chunks=[item.chunk for item in result.chunks])
