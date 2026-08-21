"""
Context manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.context.models import (
    ContextWindow,
)

if TYPE_CHECKING:
    from ai_team.context.compressor import ContextCompressor
    from ai_team.context.selector import ContextSelector
    from ai_team.context.summarizer import ContextSummarizer
    from ai_team.graph.state import GraphState


class ContextManager:
    """
    Builds the context sent to an agent.
    """

    def __init__(
        self,
        *,
        selector: ContextSelector,
        compressor: ContextCompressor,
        summarizer: ContextSummarizer,
    ) -> None:

        self._selector = selector
        self._compressor = compressor
        self._summarizer = summarizer

    async def build(
        self,
        state: GraphState,
    ) -> ContextWindow:
        """
        Build the complete context window.
        """

        selection = await self._selector.select(
            state,
        )

        selection = await self._compressor.compress(
            selection,
        )

        return ContextWindow(
            system_prompt=state.conversation.system_prompt,
            conversation=selection.conversation,
            memory=selection.memories,
            documents=selection.documents,
            artifacts=state.artifacts.shared_files,
        )

    async def summarize(
        self,
        state: GraphState,
    ) -> str:
        """
        Summarize the current conversation.
        """

        summary = await self._summarizer.summarize(
            state.conversation.conversation_history,
        )

        return summary.summary
