"""
Metadata extraction utilities.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.rag.models import (
        Document,
        DocumentMetadata,
    )


class MetadataExtractor:
    """
    Extracts metadata from documents.
    """

    def extract(
        self,
        document: Document,
    ) -> DocumentMetadata:
        """
        Extract metadata.

        Future implementations may enrich metadata with:

            - language detection
            - file type
            - repository
            - branch
            - author
            - timestamps
        """

        return document.metadata
