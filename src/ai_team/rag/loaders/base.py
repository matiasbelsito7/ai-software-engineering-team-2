"""
Base document loader interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.rag.models import (
        Document,
        DocumentSource,
    )


class BaseDocumentLoader(ABC):
    """
    Contract implemented by every document loader.
    """

    @abstractmethod
    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        """
        Load a single document from the given source.
        """
        raise NotImplementedError
