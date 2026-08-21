"""
Conversation summarizer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

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

        The current implementation uses a placeholder prompt.
        """

        prompt = (
            "Summarize the following conversation:\n\n"
            + "\n".join(conversation)
        )

        conv = Conversation()
        conv.add_user(prompt)

        response = await self._llm.generate(
            conv,
        )

        return ContextSummary(
            summary=response.content,
            source_messages=len(
                conversation,
            ),
            compression_ratio=0.0,
        )
