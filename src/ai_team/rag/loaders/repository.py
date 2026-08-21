"""
Repository loader.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.loaders.base import BaseDocumentLoader

if TYPE_CHECKING:
    from ai_team.rag.models import (
        Document,
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
