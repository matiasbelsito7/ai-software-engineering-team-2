"""
Memory reranker.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryEntry,
        MemoryQuery,
    )


class MemoryReranker:
    """
    Reorders retrieved memories according to relevance.

    Uses a simple heuristic: exact token overlap with the query,
    penalising very short entries, and preferring entries with
    higher original scores.

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
        query_lower = query.query.lower()
        query_tokens = set(query_lower.split())

        def _relevance(entry: MemoryEntry) -> float:
            content_lower = entry.content.lower()
            content_tokens = set(content_lower.split())

            overlap = len(query_tokens & content_tokens)
            token_score = overlap / max(len(query_tokens), 1)

            exact_bonus = 0.2 if query_lower in content_lower else 0.0

            length_penalty = min(len(content_lower) / 500.0, 0.1)

            return entry.score * 0.4 + token_score * 0.4 + exact_bonus + length_penalty

        return sorted(entries, key=_relevance, reverse=True)
