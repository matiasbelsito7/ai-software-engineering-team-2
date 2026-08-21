"""
Markdown document loader.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.rag.loaders.base import (
    BaseDocumentLoader,
)
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)


class MarkdownLoader(BaseDocumentLoader):
    """
    Loads Markdown documents from the local filesystem.
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        """
        Load a Markdown document.
        """

        path = Path(source.uri)

        content = path.read_text(
            encoding="utf-8",
        )

        metadata = DocumentMetadata(
            title=source.title or path.stem,
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )
