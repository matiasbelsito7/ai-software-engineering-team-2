"""
Base interface for vector stores.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai_team.rag.models import (
    DocumentChunk,
    RetrievedChunk,
)


class BaseVectorStore(ABC):
    """
    Base interface implemented by every vector database.
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    async def initialize(
        self,
    ) -> None:
        """
        Initialize the vector store.

        This may include creating collections,
        indexes or validating the schema.
        """
        ...

    @abstractmethod
    async def health(
        self,
    ) -> bool:
        """
        Check whether the vector store is available.
        """
        ...

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    @abstractmethod
    async def upsert(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Insert or update document chunks.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete every chunk belonging to a document.
        """
        ...

    @abstractmethod
    async def clear(
        self,
    ) -> None:
        """
        Remove every stored chunk.
        """
        ...

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    @abstractmethod
    async def search(
        self,
        *,
        embedding: list[float],
        limit: int,
    ) -> list[RetrievedChunk]:
        """
        Search the nearest document chunks for an embedding.
        """
        ...