"""
LLM cost tracker.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, ClassVar

from ai_team.shared.enums.observability import (
    LLMProvider,
)

if TYPE_CHECKING:
    from ai_team.observability.models import LLMCall


class CostTracker:
    """
    Tracks accumulated LLM costs.

    Prices are expressed in USD per 1M tokens.
    """

    DEFAULT_PRICES: ClassVar[dict[str, tuple[float, float]]] = {

        #
        # OpenAI
        #

        "gpt-5.5": (
            2.00,
            8.00,
        ),

        "gpt-5.5-mini": (
            0.40,
            1.60,
        ),

        #
        # Embeddings
        #

        "text-embedding-3-small": (
            0.02,
            0.02,
        ),

        "text-embedding-3-large": (
            0.13,
            0.13,
        ),
    }

    def __init__(
        self,
    ) -> None:

        self._total_cost = 0.0

        self._agent_costs: defaultdict[
            str,
            float,
        ] = defaultdict(float)

    async def record(
        self,
        call: LLMCall,
    ) -> None:
        """
        Record one LLM invocation.
        """

        if (
            call.provider
            == LLMProvider.OLLAMA
        ):
            return

        if (
            call.model
            not in self.DEFAULT_PRICES
        ):
            return

        prompt_price, completion_price = (
            self.DEFAULT_PRICES[
                call.model
            ]
        )

        cost = (
            (call.prompt_tokens / 1_000_000)
            * prompt_price
        ) + (
            (
                call.completion_tokens
                / 1_000_000
            )
            * completion_price
        )

        self._total_cost += cost

        self._agent_costs[
            str(call.agent)
        ] += cost

    @property
    def total_cost(
        self,
    ) -> float:
        return self._total_cost

    def cost_by_agent(
        self,
    ) -> dict[str, float]:

        return dict(
            self._agent_costs,
        )

    def reset(
        self,
    ) -> None:

        self._total_cost = 0.0

        self._agent_costs.clear()
