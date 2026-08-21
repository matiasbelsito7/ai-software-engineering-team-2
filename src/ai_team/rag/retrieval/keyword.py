"""
Keyword retriever using TF-IDF-inspired scoring.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import TYPE_CHECKING

from ai_team.rag.models import (
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
)
from ai_team.rag.retrieval.base import BaseRetriever

if TYPE_CHECKING:
    from ai_team.rag.models import DocumentChunk
    from ai_team.rag.stores.base import BaseVectorStore


def _tokenize(text: str) -> list[str]:
    """Lowercase and split text into word tokens."""

    return re.findall(r"[a-z0-9_]{2,}", text.lower())


def _tf(tokens: list[str]) -> dict[str, float]:
    """Term frequency normalized by document length."""

    counts = Counter(tokens)
    length = len(tokens) or 1

    return {term: count / length for term, count in counts.items()}


class KeywordRetriever(BaseRetriever):
    """
    Keyword-based retrieval using TF scoring and query term overlap.

    Operates on the raw content stored in the vector store.
    For the in-memory store, this scans all chunks directly.
    """

    def __init__(
        self,
        *,
        store: BaseVectorStore | None = None,
    ) -> None:
        self._store = store

    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        chunks = self._get_chunks()

        if not chunks:
            return RetrievalResult(query=query, chunks=[])

        query_tokens = _tokenize(query.query)
        query_tf = _tf(query_tokens)

        scored: list[tuple[float, DocumentChunk]] = []

        for chunk in chunks:
            doc_tokens = _tokenize(chunk.content)
            doc_tf = _tf(doc_tokens)

            score = sum(query_tf.get(term, 0.0) * doc_tf.get(term, 0.0) for term in query_tf)

            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)

        return RetrievalResult(
            query=query,
            chunks=[RetrievedChunk(chunk=c, score=s) for s, c in scored[: query.top_k]],
        )

    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        result = await self.search(query)

        return RAGContext(chunks=[item.chunk for item in result.chunks])

    def _get_chunks(self) -> list[DocumentChunk]:
        """Extract stored chunks from the vector store."""

        if self._store is None:
            return []

        chunks = getattr(self._store, "_chunks", None)

        if chunks is not None:
            return list(chunks)

        return []
