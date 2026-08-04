"""
Memory reranker.
"""

from __future__ import annotations

from ai_team.memory.models import (
    MemoryEntry,
    MemoryQuery,
)


class MemoryReranker:
    """
    Reorders retrieved memories according to relevance.

    Future implementations may use:
        - CrossEncoder
        - Cohere Rerank
        - BGE Reranker
        - LLM-based reranking
    """

    async def rerank(
        self,
        *,
        query: MemoryQuery,
        entries: list[MemoryEntry],
    ) -> list[MemoryEntry]:
        """
        Rerank retrieved memories.

        Current implementation keeps the original order.
        """

        return entries