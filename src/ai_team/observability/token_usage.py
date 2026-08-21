"""
Token usage tracker.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.observability.models import LLMCall


class TokenUsageTracker:
    """
    Tracks token consumption.
    """

    def __init__(self) -> None:

        self._prompt_tokens = 0

        self._completion_tokens = 0

        self._agent_usage: defaultdict[
            str,
            int,
        ] = defaultdict(int)

    async def record(
        self,
        call: LLMCall,
    ) -> None:
        """
        Record token usage from one LLM call.
        """

        self._prompt_tokens += call.prompt_tokens

        self._completion_tokens += (
            call.completion_tokens
        )

        self._agent_usage[
            str(call.agent)
        ] += call.total_tokens

    @property
    def prompt_tokens(
        self,
    ) -> int:
        return self._prompt_tokens

    @property
    def completion_tokens(
        self,
    ) -> int:
        return self._completion_tokens

    @property
    def total_tokens(
        self,
    ) -> int:
        return (
            self._prompt_tokens
            + self._completion_tokens
        )

    def usage_by_agent(
        self,
    ) -> dict[str, int]:

        return dict(self._agent_usage)

    def reset(
        self,
    ) -> None:

        self._prompt_tokens = 0

        self._completion_tokens = 0

        self._agent_usage.clear()
