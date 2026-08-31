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


class BudgetExhaustedError(Exception):
    """Raised when the token budget is exhausted."""

    def __init__(self, tokens_used: int, budget: int) -> None:
        self.tokens_used = tokens_used
        self.budget = budget
        super().__init__(f"Budget exhausted: {tokens_used}/{budget} tokens used")


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

        # Budget enforcement
        self._token_budget: int | None = None
        self._tokens_used: int = 0
        self._budget_enforcement_enabled: bool = False

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
    # Budget enforcement
    # ---------------------------------------------------------

    def set_token_budget(self, budget: int | None) -> None:
        """
        Set the token budget for this tracking session.

        If None, budget enforcement is disabled.
        """
        self._token_budget = budget
        self._budget_enforcement_enabled = budget is not None and budget > 0

    def check_budget(self, additional_tokens: int = 0) -> bool:
        """
        Check if the budget can accommodate additional tokens.

        Returns True if within budget, False if exceeded.
        """
        if not self._budget_enforcement_enabled or self._token_budget is None:
            return True

        return (self._tokens_used + additional_tokens) <= self._token_budget

    def get_remaining_budget(self) -> int | None:
        """
        Get remaining token budget.

        Returns None if budget enforcement is disabled.
        """
        if not self._budget_enforcement_enabled or self._token_budget is None:
            return None

        return max(0, self._token_budget - self._tokens_used)

    def get_usage_percentage(self) -> float | None:
        """
        Get budget usage as a percentage (0-100).

        Returns None if budget enforcement is disabled.
        """
        if not self._budget_enforcement_enabled or self._token_budget is None:
            return None

        if self._token_budget == 0:
            return 100.0

        return (self._tokens_used / self._token_budget) * 100

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

        # Track tokens for budget enforcement
        call_tokens = call.prompt_tokens + call.completion_tokens
        self._tokens_used += call_tokens

        # Check budget
        if self._budget_enforcement_enabled and not self.check_budget(0):
            raise BudgetExhaustedError(
                self._tokens_used,
                self._token_budget or 0,
            )

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

    @property
    def tokens_used(self) -> int:
        return self._tokens_used

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
        self._tokens_used = 0
        self._agent_costs.clear()
