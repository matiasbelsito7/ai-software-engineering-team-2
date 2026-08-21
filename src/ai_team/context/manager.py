"""
Context manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.context.exceptions import (
    ContextCompressionError,
    ContextSelectionError,
    ContextSummarizationError,
)
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

        try:
            selection = await self._selector.select(state)
        except Exception as exc:
            raise ContextSelectionError(
                f"Context selection failed: {exc}",
            ) from exc

        try:
            selection = await self._compressor.compress(selection)
        except ContextCompressionError:
            raise
        except Exception as exc:
            raise ContextCompressionError(
                f"Context compression failed: {exc}",
            ) from exc

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

        try:
            summary = await self._summarizer.summarize(
                state.conversation.conversation_history,
            )
        except ContextSummarizationError:
            raise
        except Exception as exc:
            raise ContextSummarizationError(
                f"Context summarization failed: {exc}",
            ) from exc

        return summary.summary
