"""
Base interface for vector stores.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai_team.rag.models import (
    Document,
    DocumentChunk,
    RetrievalQuery,
    RetrievalResult,
)


class BaseVectorStore(ABC):
    """
    Base interface implemented by every vector store.
    """

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    @abstractmethod
    async def index(
        self,
        document: Document,
    ) -> None:
        """
        Index a document.
        """
        ...

    @abstractmethod
    async def upsert(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Insert or update document chunks.
        """
        ...

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    @abstractmethod
    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Perform semantic similarity search.
        """
        ...

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    @abstractmethod
    async def get(
        self,
        document_id: str,
    ) -> Document | None:
        """
        Retrieve a document by its identifier.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.
        """
        ...

    @abstractmethod
    async def clear(self) -> None:
        """
        Remove every indexed document.
        """
        ...

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @abstractmethod
    async def exists(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether a document exists.
        """
        ...