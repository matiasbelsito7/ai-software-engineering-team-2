"""
Document indexing pipeline.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.rag.embedding.base import (
        BaseEmbeddingProvider,
    )
    from ai_team.rag.indexing.chunking import (
        ChunkingPipeline,
    )
    from ai_team.rag.models import (
        Document,
        DocumentChunk,
    )


class IndexingPipeline:
    """
    Produces embedded document chunks.
    """

    def __init__(
        self,
        *,
        chunking: ChunkingPipeline,
        embedding: BaseEmbeddingProvider,
    ) -> None:
        self._chunking = chunking
        self._embedding = embedding

    async def process(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        """
        Convert a document into embedded chunks.
        """

        chunks = self._chunking.process(
            document,
        )

        embeddings = await self._embedding.embed_batch(
            [
                chunk.content
                for chunk in chunks
            ]
        )

        return [
            chunk.model_copy(
                update={
                    "embedding": embedding,
                }
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            )
        ]
