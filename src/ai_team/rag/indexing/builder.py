"""
Document chunk builder.
"""

from __future__ import annotations

from ai_team.rag.models import (
    Document,
    DocumentChunk,
    DocumentMetadata,
)


class DocumentChunkBuilder:
    """
    Builds DocumentChunk instances from chunked text.
    """

    def build(
        self,
        *,
        document: Document,
        chunks: list[str],
        metadata: DocumentMetadata,
    ) -> list[DocumentChunk]:
        """
        Build document chunks.
        """

        return [
            DocumentChunk(
                document_id=document.id,
                uri=document.source.uri,
                source_type=document.source.type,
                content=chunk,
                metadata=metadata,
                chunk_index=index,
            )
            for index, chunk in enumerate(chunks)
        ]