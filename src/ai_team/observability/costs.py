"""
LLM cost tracker.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, ClassVar

from ai_team.observability.exceptions import CostCalculationError
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

        self._custom_prices: dict[str, tuple[float, float]] = {}

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def set_price(
        self,
        model: str,
        prompt_price: float,
        completion_price: float,
    ) -> None:
        """
        Override or add a price entry for a model.

        Prices are in USD per 1M tokens.
        """

        if prompt_price < 0 or completion_price < 0:
            raise CostCalculationError(
                f"Prices must be non-negative, got prompt={prompt_price}, "
                f"completion={completion_price}",
            )

        self._custom_prices[model] = (prompt_price, completion_price)

    def get_price(
        self,
        model: str,
    ) -> tuple[float, float] | None:
        """
        Look up the price for a model.

        Returns (prompt_price, completion_price) or None if unknown.
        """

        if model in self._custom_prices:
            return self._custom_prices[model]

        return self.DEFAULT_PRICES.get(model)

    # ---------------------------------------------------------
    # Recording
    # ---------------------------------------------------------

    async def record(
        self,
        call: LLMCall,
    ) -> None:
        """
        Record one LLM invocation.
        """

        if call.provider == LLMProvider.OLLAMA:
            return

        prices = self.get_price(call.model)

        if prices is None:
            return

        prompt_price, completion_price = prices

        cost = ((call.prompt_tokens / 1_000_000) * prompt_price) + (
            (call.completion_tokens / 1_000_000) * completion_price
        )

        self._total_cost += cost

        self._agent_costs[str(call.agent)] += cost

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
