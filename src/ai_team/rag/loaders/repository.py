"""
Repository loader.
"""

from __future__ import annotations

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)


class RepositoryLoader(BaseDocumentLoader):
    """
    Loads an entire software repository.

    Future implementation may aggregate:

        - README
        - source code
        - documentation
        - ADRs
        - configuration files
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        """
        Load repository contents.
        """

        raise NotImplementedError