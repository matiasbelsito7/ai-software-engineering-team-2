"""
Conversation summarizer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.context.exceptions import ContextSummarizationError
from ai_team.context.models import (
    ContextSummary,
)
from ai_team.infrastructure.llm.messages import (
    Conversation,
)

if TYPE_CHECKING:
    from ai_team.infrastructure.llm.base import BaseLLM


class ContextSummarizer:
    """
    Produces semantic summaries of conversations.
    """

    def __init__(
        self,
        *,
        llm: BaseLLM,
    ) -> None:

        self._llm = llm

    async def summarize(
        self,
        conversation: list[str],
    ) -> ContextSummary:
        """
        Summarize a conversation.

        Uses the LLM to produce a concise summary.  Returns an
        empty summary for empty conversations.
        """

        if not conversation:
            return ContextSummary(
                summary="",
                source_messages=0,
                compression_ratio=1.0,
            )

        try:
            prompt = (
                "You are a conversation summarizer. "
                "Produce a concise summary of the following conversation, "
                "preserving key decisions, actions, and context.\n\n" + "\n".join(conversation)
            )

            conv = Conversation()
            conv.add_user(prompt)

            response = await self._llm.generate(conv)

            original_chars = sum(len(m) for m in conversation)
            summary_chars = len(response.content)

            ratio = summary_chars / original_chars if original_chars > 0 else 1.0

            return ContextSummary(
                summary=response.content,
                source_messages=len(conversation),
                compression_ratio=round(ratio, 4),
            )
        except ContextSummarizationError:
            raise
        except Exception as exc:
            raise ContextSummarizationError(
                f"Failed to summarize conversation: {exc}",
            ) from exc
