"""
Semantic document retriever.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import (
    BaseRetriever,
)

if TYPE_CHECKING:
    from ai_team.rag.embedding.base import BaseEmbeddingProvider
    from ai_team.rag.stores.base import (
        BaseVectorStore,
    )


class SemanticRetriever(BaseRetriever):
    """
    Semantic similarity retriever.

    Embeds the query, then delegates vector search to the store.
    """

    def __init__(
        self,
        *,
        store: BaseVectorStore,
        embedding: BaseEmbeddingProvider,
    ) -> None:
        self._store = store
        self._embedding = embedding

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        embedding = await self._embedding.embed(
            query.query,
        )

        chunks = await self._store.search(
            embedding=embedding,
            limit=query.top_k,
        )

        return RetrievalResult(
            query=query,
            chunks=chunks,
        )

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        result = await self.search(
            query,
        )

        return RAGContext(chunks=[item.chunk for item in result.chunks])
