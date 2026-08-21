"""
Git repository loader.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.loaders.base import BaseDocumentLoader

if TYPE_CHECKING:
    from ai_team.rag.models import (
        Document,
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
