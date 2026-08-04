"""
High-level RAG manager.
"""

from __future__ import annotations

from ai_team.rag.indexing.pipeline import (
    IndexingPipeline,
)
from ai_team.rag.models import (
    Document,
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.base import (
    BaseRetriever,
)
from ai_team.rag.stores.base import (
    BaseVectorStore,
)


class RAGManager:
    """
    Coordinates document indexing and retrieval.
    """

    def __init__(
        self,
        *,
        pipeline: IndexingPipeline,
        store: BaseVectorStore,
        retriever: BaseRetriever,
    ) -> None:
        self._pipeline = pipeline
        self._store = store
        self._retriever = retriever

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    async def index(
        self,
        document: Document,
    ) -> None:
        """
        Index a document.
        """

        chunks = await self._pipeline.process(
            document,
        )

        await self._store.upsert(
            chunks,
        )

    async def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.
        """

        await self._store.delete(
            document_id,
        )

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Retrieve relevant chunks.
        """

        return await self._retriever.search(
            query,
        )

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        """
        Build context for an agent.
        """

        return await self._retriever.build_context(
            query,
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    async def clear(
        self,
    ) -> None:
        """
        Remove every indexed document.
        """

        await self._store.clear()