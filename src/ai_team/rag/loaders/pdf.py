"""
PDF document loader.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)


class PDFLoader(BaseDocumentLoader):
    """
    Loads PDF documents.

    Future implementation:
        pypdf
        pymupdf
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:

        path = Path(source.uri)

        #
        # TODO:
        # Extract PDF text.
        #

        content = ""

        metadata = DocumentMetadata(
            title=source.title or path.stem,
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )
