from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.models import RetrievedChunk
from ai_team.rag.stores.base import BaseVectorStore

if TYPE_CHECKING:
    from ai_team.rag.models import DocumentChunk


class InMemoryVectorStore(BaseVectorStore):

    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []

    async def initialize(self) -> None:
        pass

    async def health(self) -> bool:
        return True

    async def upsert(self, chunks: list[DocumentChunk]) -> None:
        self._chunks.extend(chunks)

    async def delete(self, document_id: str) -> None:
        self._chunks = [c for c in self._chunks if str(c.document_id) != document_id]

    async def clear(self) -> None:
        self._chunks.clear()

    async def search(self, *, embedding: list[float], limit: int) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(chunk=c, score=0.0)
            for c in self._chunks[:limit]
        ]
