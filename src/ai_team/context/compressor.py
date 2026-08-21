"""
Context compressor.
"""

from __future__ import annotations

from ai_team.context.models import ContextSelection


class ContextCompressor:
    """
    Compresses the selected context so that it fits
    within the target context window.
    """

    def __init__(
        self,
        *,
        max_messages: int = 15,
        max_memories: int = 8,
        max_documents: int = 8,
    ) -> None:

        self._max_messages = max_messages

        self._max_memories = max_memories

        self._max_documents = max_documents

    async def compress(
        self,
        selection: ContextSelection,
    ) -> ContextSelection:
        """
        Compress the context.

        Current implementation performs heuristic truncation.
        """

        return ContextSelection(
            conversation=selection.conversation[-self._max_messages :],
            memories=selection.memories[: self._max_memories],
            documents=selection.documents[: self._max_documents],
            metadata=selection.metadata,
        )
