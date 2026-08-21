"""
Keyword retrieval strategy with TF-IDF-style scoring.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING

from ai_team.memory.models import (
    MemoryContext,
    MemoryQuery,
    MemorySearchResult,
)
from ai_team.memory.retrieval.base import BaseRetriever

if TYPE_CHECKING:
    from ai_team.memory.models import MemoryEntry
    from ai_team.memory.stores.base import BaseMemoryStore


_STOPWORDS = frozenset(
    {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "shall",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "and",
        "but",
        "or",
        "nor",
        "not",
        "so",
        "yet",
        "both",
        "either",
        "neither",
        "each",
        "every",
        "all",
        "any",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "only",
        "own",
        "same",
        "than",
        "too",
        "very",
        "just",
        "that",
        "this",
        "these",
        "those",
        "it",
        "its",
        "i",
        "me",
        "my",
        "we",
        "our",
        "you",
        "your",
        "he",
        "him",
        "his",
        "she",
        "her",
        "they",
        "them",
        "their",
    },
)


def _tokenize(text: str) -> list[str]:
    """Lowercase tokenization with stopword removal."""
    return [w for w in text.lower().split() if len(w) > 1 and w not in _STOPWORDS]


def _tfidf_score(
    query_tokens: list[str],
    doc_tokens: list[str],
    idf: dict[str, float],
) -> float:
    """Compute a TF-IDF-inspired relevance score."""
    if not query_tokens:
        return 0.0
    doc_counter = Counter(doc_tokens)
    total = len(doc_tokens) or 1
    score = 0.0
    for token in query_tokens:
        tf = doc_counter.get(token, 0) / total
        score += tf * idf.get(token, 1.0)
    return score / len(query_tokens)


class KeywordRetriever(BaseRetriever):
    """
    Retrieves memories using TF-IDF-style keyword scoring.

    Tokens from the query are matched against tokens in each stored
    entry.  The score is the fraction of query tokens found in the
    entry content, weighted by inverse document frequency.
    """

    def __init__(self, store: BaseMemoryStore) -> None:
        self._store = store
        self._doc_freq: Counter[str] = Counter()
        self._n_docs: int = 0

    # ------------------------------------------------------------------
    # Index building
    # ------------------------------------------------------------------

    async def _rebuild_index(self, entries: list[MemoryEntry]) -> None:
        self._doc_freq = Counter()
        self._n_docs = len(entries)
        for entry in entries:
            unique = set(_tokenize(entry.content))
            for token in unique:
                self._doc_freq[token] += 1

    def _build_idf(self) -> dict[str, float]:
        return {
            token: math.log((self._n_docs + 1) / (df + 1)) + 1.0
            for token, df in self._doc_freq.items()
        }

    # ------------------------------------------------------------------
    # BaseRetriever
    # ------------------------------------------------------------------

    async def search(self, query: MemoryQuery) -> MemorySearchResult:
        all_entries_result = await self._store.search(query)
        entries = all_entries_result.entries

        if not entries:
            return MemorySearchResult(query=query, entries=[])

        await self._rebuild_index(entries)
        idf = self._build_idf()
        query_tokens = _tokenize(query.query)

        scored: list[tuple[float, MemoryEntry]] = []
        for entry in entries:
            doc_tokens = _tokenize(entry.content)
            score = _tfidf_score(query_tokens, doc_tokens, idf)
            scored.append((score, entry))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        results = [entry for _, entry in scored][: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def build_context(self, query: MemoryQuery) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)
