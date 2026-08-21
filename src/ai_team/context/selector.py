"""
Context selector.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.context.models import (
    ContextSelection,
)

if TYPE_CHECKING:
    from ai_team.graph.state import GraphState


class ContextSelector:
    """
    Selects the most relevant context.
    """

    def __init__(
        self,
        *,
        max_messages: int = 20,
        max_memories: int = 10,
        max_documents: int = 10,
    ) -> None:

        self._max_messages = max_messages

        self._max_memories = max_memories

        self._max_documents = max_documents

    async def select(
        self,
        state: GraphState,
    ) -> ContextSelection:
        """
        Select the relevant context.

        Current implementation is heuristic.
        """

        conversation = state.conversation.conversation_history[-self._max_messages :]

        memories: list[str] = []

        if state.memory is not None:
            memories = [entry.content for entry in state.memory.entries[: self._max_memories]]

        documents: list[str] = []

        if state.rag is not None:
            documents = [chunk.content for chunk in state.rag.chunks[: self._max_documents]]

        return ContextSelection(
            conversation=conversation,
            memories=memories,
            documents=documents,
        )
