"""
Document indexing pipeline.
"""

from __future__ import annotations

from ai_team.rag.embedding.base import (
    BaseEmbeddingProvider,
)
from ai_team.rag.indexing.builder import (
    DocumentChunkBuilder,
)
from ai_team.rag.indexing.chunker import (
    DocumentChunker,
)
from ai_team.rag.indexing.cleaner import (
    DocumentCleaner,
)
from ai_team.rag.indexing.metadata import (
    MetadataExtractor,
)
from ai_team.rag.indexing.splitter import (
    DocumentSplitter,
)
from ai_team.rag.models import (
    Document,
    DocumentChunk,
)


class IndexingPipeline:
    """
    Complete document indexing pipeline.
    """

    def __init__(
        self,
        *,
        cleaner: DocumentCleaner,
        splitter: DocumentSplitter,
        chunker: DocumentChunker,
        metadata: MetadataExtractor,
        builder: DocumentChunkBuilder,
        embedding: BaseEmbeddingProvider,
    ) -> None:
        self._cleaner = cleaner
        self._splitter = splitter
        self._chunker = chunker
        self._metadata = metadata
        self._builder = builder
        self._embedding = embedding

    async def process(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        """
        Process a document into embedded chunks.
        """

        cleaned = self._cleaner.clean(
            document.content,
        )

        sections = self._splitter.split(
            cleaned,
        )

        chunks = self._chunker.chunk(
            sections,
        )

        metadata = self._metadata.extract(
            document,
        )

        documents = self._builder.build(
            document=document,
            chunks=chunks,
            metadata=metadata,
        )

        embeddings = await self._embedding.embed_batch(
            [chunk.content for chunk in documents]
        )

        return [
            chunk.model_copy(
                update={
                    "embedding": embedding,
                }
            )
            for chunk, embedding in zip(
                documents,
                embeddings,
                strict=True,
            )
        ]