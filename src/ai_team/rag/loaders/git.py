"""
Git repository loader.
"""

from __future__ import annotations

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)


class GitLoader(BaseDocumentLoader):
    """
    Loads information from a Git repository.

    Future implementation may extract:

        - commits
        - branches
        - tags
        - authors
        - history
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        """
        Load Git metadata.
        """

        raise NotImplementedError