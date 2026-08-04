"""
Semantic document retriever.
"""

from __future__ import annotations

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.stores.base import (
    BaseVectorStore,
)
from ai_team.rag.retrieval.base import (
    BaseRetriever,
)


class SemanticRetriever(BaseRetriever):
    """
    Semantic similarity retriever.

    Delegates vector search to the configured vector store.
    """

    def __init__(
        self,
        *,
        store: BaseVectorStore,
    ) -> None:
        self._store = store

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Perform semantic retrieval.
        """

        return await self._store.search(
            query,
        )

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        """
        Build the prompt context.
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