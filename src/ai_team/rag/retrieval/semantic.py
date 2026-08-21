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
    from ai_team.rag.stores.base import (
        BaseVectorStore,
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

        raise NotImplementedError

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
