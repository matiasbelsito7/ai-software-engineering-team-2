"""
Document chunking pipeline.
"""

from __future__ import annotations

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


class ChunkingPipeline:
    """
    Converts a document into chunks.

    This pipeline performs:

    - cleaning
    - splitting
    - chunking
    - metadata extraction
    - chunk construction
    """

    def __init__(
        self,
        *,
        cleaner: DocumentCleaner,
        splitter: DocumentSplitter,
        chunker: DocumentChunker,
        metadata: MetadataExtractor,
        builder: DocumentChunkBuilder,
    ) -> None:
        self._cleaner = cleaner
        self._splitter = splitter
        self._chunker = chunker
        self._metadata = metadata
        self._builder = builder

    def process(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        """
        Produce chunks from a document.
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

        return self._builder.build(
            document=document,
            chunks=chunks,
            metadata=metadata,
        )