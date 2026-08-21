"""
In-memory vector store with cosine similarity search.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ai_team.rag.models import RetrievedChunk
from ai_team.rag.stores.base import BaseVectorStore

if TYPE_CHECKING:
    from ai_team.rag.models import DocumentChunk


def _cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:
    """Compute cosine similarity between two vectors."""

    if len(a) != len(b) or len(a) == 0:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


class InMemoryVectorStore(BaseVectorStore):
    """
    In-memory vector store using brute-force cosine similarity.
    """

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

    async def search(
        self,
        *,
        embedding: list[float],
        limit: int,
    ) -> list[RetrievedChunk]:
        if not self._chunks or not embedding:
            return []

        scored: list[tuple[float, DocumentChunk]] = []

        for chunk in self._chunks:
            if chunk.embedding is not None:
                score = _cosine_similarity(embedding, chunk.embedding)
            else:
                score = 0.0
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [RetrievedChunk(chunk=c, score=s) for s, c in scored[:limit]]
