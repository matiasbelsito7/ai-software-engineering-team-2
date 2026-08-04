"""
Python source loader.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)


class PythonLoader(BaseDocumentLoader):
    """
    Loads Python source files.

    Future implementations may also extract:

        - classes
        - functions
        - docstrings
        - imports
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:

        path = Path(source.uri)

        content = path.read_text(
            encoding="utf-8",
        )

        metadata = DocumentMetadata(
            title=source.title or path.stem,
            language="python",
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )