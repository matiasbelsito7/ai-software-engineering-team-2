"""
Qdrant vector store.

Future implementation:
    qdrant-client
"""

from __future__ import annotations

from ai_team.rag.models import (
    Document,
    DocumentChunk,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.stores.base import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    """
    Vector store backed by Qdrant.
    """

    async def index(
        self,
        document: Document,
    ) -> None:
        raise NotImplementedError

    async def upsert(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        raise NotImplementedError

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        raise NotImplementedError

    async def get(
        self,
        document_id: str,
    ) -> Document | None:
        raise NotImplementedError

    async def delete(
        self,
        document_id: str,
    ) -> None:
        raise NotImplementedError

    async def clear(
        self,
    ) -> None:
        raise NotImplementedError

    async def exists(
        self,
        document_id: str,
    ) -> bool:
        raise NotImplementedError