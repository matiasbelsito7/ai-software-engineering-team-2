"""
Conversation summarizer.
"""

from __future__ import annotations

from ai_team.context.models import (
    ContextSummary,
)
from ai_team.llm.base import BaseLLMProvider


class ContextSummarizer:
    """
    Produces semantic summaries of conversations.
    """

    def __init__(
        self,
        *,
        llm: BaseLLMProvider,
    ) -> None:

        self._llm = llm

    async def summarize(
        self,
        conversation: list[str],
    ) -> ContextSummary:
        """
        Summarize a conversation.

        The current implementation uses a placeholder prompt.
        """

        prompt = (
            "Summarize the following conversation:\n\n"
            + "\n".join(conversation)
        )

        response = await self._llm.generate(
            prompt=prompt,
        )

        return ContextSummary(
            summary=response.text,
            source_messages=len(
                conversation,
            ),
            compression_ratio=0.0,
        )