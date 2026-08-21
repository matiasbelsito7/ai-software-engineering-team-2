"""
RAG module factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.indexing.pipeline import IndexingPipeline
from ai_team.rag.manager import RAGManager
from ai_team.rag.retrieval.hybrid import HybridRetriever

if TYPE_CHECKING:
    from ai_team.rag.embedding.base import BaseEmbeddingProvider
    from ai_team.rag.indexing.chunking import ChunkingPipeline
    from ai_team.rag.retrieval.base import BaseRetriever
    from ai_team.rag.stores.base import BaseVectorStore


def build_rag(
    *,
    chunking: ChunkingPipeline,
    embedding: BaseEmbeddingProvider,
    semantic: BaseRetriever,
    keyword: BaseRetriever,
    store: BaseVectorStore,
) -> RAGManager:
    """
    Build the RAG subsystem.
    """

    indexing = IndexingPipeline(
        chunking=chunking,
        embedding=embedding,
    )

    retrieval = HybridRetriever(
        semantic=semantic,
        keyword=keyword,
    )

    return RAGManager(
        pipeline=indexing,
        store=store,
        retriever=retrieval,
    )
