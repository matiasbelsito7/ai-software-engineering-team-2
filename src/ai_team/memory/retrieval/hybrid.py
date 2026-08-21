"""
Hybrid retrieval strategy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.memory.models import (
    MemoryContext,
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
)
from ai_team.memory.retrieval.base import BaseRetriever

if TYPE_CHECKING:
    from ai_team.memory.retrieval.keyword import KeywordRetriever
    from ai_team.memory.retrieval.reranker import MemoryReranker
    from ai_team.memory.retrieval.semantic import SemanticRetriever


def _rrf_score(rank: int, k: int = 60) -> float:
    """Reciprocal Rank Fusion score."""
    return 1.0 / (k + rank)


class HybridRetriever(BaseRetriever):
    """
    Combines semantic and keyword retrieval using Reciprocal Rank Fusion.
    """

    def __init__(
        self,
        *,
        semantic: SemanticRetriever,
        keyword: KeywordRetriever,
        reranker: MemoryReranker | None = None,
    ) -> None:
        self._semantic = semantic
        self._keyword = keyword
        self._reranker = reranker

    async def search(self, query: MemoryQuery) -> MemorySearchResult:
        semantic_result = await self._semantic.search(query)
        keyword_result = await self._keyword.search(query)

        # Reciprocal Rank Fusion
        rrf_scores: dict[str, float] = {}
        entry_map: dict[str, MemoryEntry] = {}

        for rank, entry in enumerate(semantic_result.entries):
            eid = str(entry.id)
            rrf_scores[eid] = rrf_scores.get(eid, 0.0) + _rrf_score(rank + 1)
            entry_map[eid] = entry

        for rank, entry in enumerate(keyword_result.entries):
            eid = str(entry.id)
            rrf_scores[eid] = rrf_scores.get(eid, 0.0) + _rrf_score(rank + 1)
            entry_map[eid] = entry

        sorted_ids = sorted(rrf_scores, key=rrf_scores.get, reverse=True)  # type: ignore[arg-type]
        entries = [entry_map[eid] for eid in sorted_ids[: query.top_k]]

        if self._reranker is not None:
            entries = await self._reranker.rerank(
                query=query,
                entries=entries,
            )

        return MemorySearchResult(query=query, entries=entries)

    async def build_context(self, query: MemoryQuery) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)
