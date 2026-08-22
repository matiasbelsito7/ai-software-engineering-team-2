"""
Cost tracking store.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from ai_team.cost_tracking.models import (
    CostAlert,
    CostBudget,
    CostRecord,
    CostSummary,
    LLMProvider,
    ModelPricing,
)

logger = logging.getLogger(__name__)

# Default pricing for common models
DEFAULT_PRICING: list[ModelPricing] = [
    ModelPricing(
        provider=LLMProvider.OPENAI,
        model="gpt-4o",
        input_price_per_1k=0.005,
        output_price_per_1k=0.015,
    ),
    ModelPricing(
        provider=LLMProvider.OPENAI,
        model="gpt-4o-mini",
        input_price_per_1k=0.00015,
        output_price_per_1k=0.0006,
    ),
    ModelPricing(
        provider=LLMProvider.OPENAI,
        model="gpt-3.5-turbo",
        input_price_per_1k=0.0005,
        output_price_per_1k=0.0015,
    ),
    ModelPricing(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-opus-20240229",
        input_price_per_1k=0.015,
        output_price_per_1k=0.075,
    ),
    ModelPricing(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-sonnet-20240229",
        input_price_per_1k=0.003,
        output_price_per_1k=0.015,
    ),
    ModelPricing(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-haiku-20240307",
        input_price_per_1k=0.00025,
        output_price_per_1k=0.00125,
    ),
]


class CostTracker:
    """Track LLM usage costs."""

    def __init__(self) -> None:
        self._records: list[CostRecord] = []
        self._pricing: dict[tuple[str, str], ModelPricing] = {}
        self._alerts: dict[str, CostAlert] = {}
        self._budgets: dict[str, CostBudget] = {}

        # Load default pricing
        for p in DEFAULT_PRICING:
            self._pricing[(p.provider, p.model)] = p

    def set_pricing(self, pricing: ModelPricing) -> None:
        """Set pricing for a model."""
        self._pricing[(pricing.provider, pricing.model)] = pricing
        logger.info("Set pricing for %s/%s", pricing.provider, pricing.model)

    def get_pricing(self, provider: LLMProvider, model: str) -> ModelPricing | None:
        """Get pricing for a model."""
        return self._pricing.get((provider, model))

    def calculate_cost(
        self,
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> tuple[float, float, float]:
        """Calculate cost. Returns (input_cost, output_cost, total_cost)."""
        pricing = self.get_pricing(provider, model)
        if not pricing:
            logger.warning("No pricing for %s/%s, using estimates", provider, model)
            # Estimate based on rough averages
            input_cost = input_tokens * 0.001 / 1000
            output_cost = output_tokens * 0.003 / 1000
        else:
            input_cost = (input_tokens / 1000) * pricing.input_price_per_1k
            output_cost = (output_tokens / 1000) * pricing.output_price_per_1k

        total_cost = input_cost + output_cost
        return input_cost, output_cost, total_cost

    def record_usage(
        self,
        record_id: str,
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_id: str | None = None,
        agent_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CostRecord:
        """Record LLM usage."""
        input_cost, output_cost, total_cost = self.calculate_cost(
            provider, model, input_tokens, output_tokens
        )

        record = CostRecord(
            record_id=record_id,
            task_id=task_id,
            agent_name=agent_name,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            metadata=metadata or {},
        )

        self._records.append(record)
        logger.info(
            "Recorded usage: %s/%s tokens=%d cost=$%.4f",
            provider,
            model,
            record.total_tokens,
            total_cost,
        )

        # Check alerts
        self._check_alerts(record)

        # Update budgets
        self._update_budgets(record)

        return record

    def get_summary(
        self,
        task_id: str | None = None,
        agent_name: str | None = None,
        provider: LLMProvider | None = None,
        model: str | None = None,
    ) -> CostSummary:
        """Get cost summary with optional filters."""
        filtered = self._records

        if task_id:
            filtered = [r for r in filtered if r.task_id == task_id]
        if agent_name:
            filtered = [r for r in filtered if r.agent_name == agent_name]
        if provider:
            filtered = [r for r in filtered if r.provider == provider]
        if model:
            filtered = [r for r in filtered if r.model == model]

        if not filtered:
            return CostSummary()

        by_provider: dict[str, float] = defaultdict(float)
        by_model: dict[str, float] = defaultdict(float)
        by_agent: dict[str, float] = defaultdict(float)
        by_task: dict[str, float] = defaultdict(float)

        total_cost = 0.0
        total_input = 0
        total_output = 0
        total_tokens = 0

        for r in filtered:
            total_cost += r.total_cost
            total_input += r.input_tokens
            total_output += r.output_tokens
            total_tokens += r.total_tokens
            by_provider[r.provider] += r.total_cost
            by_model[r.model] += r.total_cost
            if r.agent_name:
                by_agent[r.agent_name] += r.total_cost
            if r.task_id:
                by_task[r.task_id] += r.total_cost

        return CostSummary(
            total_cost=total_cost,
            total_input_tokens=total_input,
            total_output_tokens=total_output,
            total_tokens=total_tokens,
            total_requests=len(filtered),
            by_provider=dict(by_provider),
            by_model=dict(by_model),
            by_agent=dict(by_agent),
            by_task=dict(by_task),
        )

    def list_records(
        self,
        task_id: str | None = None,
        agent_name: str | None = None,
        provider: LLMProvider | None = None,
        limit: int = 100,
    ) -> list[CostRecord]:
        """List cost records with filters."""
        filtered = self._records

        if task_id:
            filtered = [r for r in filtered if r.task_id == task_id]
        if agent_name:
            filtered = [r for r in filtered if r.agent_name == agent_name]
        if provider:
            filtered = [r for r in filtered if r.provider == provider]

        return filtered[-limit:]

    # --- Alerts ---

    def add_alert(self, alert: CostAlert) -> None:
        """Add a cost alert."""
        self._alerts[alert.alert_id] = alert
        logger.info("Added cost alert: %s", alert.alert_id)

    def get_alert(self, alert_id: str) -> CostAlert | None:
        return self._alerts.get(alert_id)

    def list_alerts(self) -> list[CostAlert]:
        return list(self._alerts.values())

    def delete_alert(self, alert_id: str) -> bool:
        if alert_id in self._alerts:
            del self._alerts[alert_id]
            return True
        return False

    def _check_alerts(self, record: CostRecord) -> None:
        """Check if any alerts should trigger."""
        from datetime import UTC, datetime

        for alert in self._alerts.values():
            if not alert.enabled or alert.triggered:
                continue

            # Filter by provider/model
            if alert.provider and record.provider != alert.provider:
                continue
            if alert.model and record.model != alert.model:
                continue

            # Get period summary
            summary = self.get_summary(provider=alert.provider, model=alert.model)
            if summary.total_cost >= alert.threshold:
                alert.triggered = True
                alert.last_triggered = datetime.now(UTC).isoformat()
                logger.warning(
                    "Cost alert '%s' triggered: $%.2f >= $%.2f",
                    alert.name,
                    summary.total_cost,
                    alert.threshold,
                )

    # --- Budgets ---

    def add_budget(self, budget: CostBudget) -> None:
        """Add a budget."""
        self._budgets[budget.budget_id] = budget
        logger.info("Added budget: %s", budget.budget_id)

    def get_budget(self, budget_id: str) -> CostBudget | None:
        return self._budgets.get(budget_id)

    def list_budgets(self) -> list[CostBudget]:
        return list(self._budgets.values())

    def delete_budget(self, budget_id: str) -> bool:
        if budget_id in self._budgets:
            del self._budgets[budget_id]
            return True
        return False

    def _update_budgets(self, record: CostRecord) -> None:
        """Update budget usage."""
        for budget in self._budgets.values():
            # Filter by provider/model
            if budget.provider and record.provider != budget.provider:
                continue
            if budget.model and record.model != budget.model:
                continue

            budget.current_usage += record.total_cost
            budget.remaining = max(0, budget.limit - budget.current_usage)
            budget.percentage_used = (
                (budget.current_usage / budget.limit * 100) if budget.limit > 0 else 0
            )

            if budget.percentage_used >= 100:
                logger.warning(
                    "Budget '%s' exceeded: $%.2f / $%.2f",
                    budget.name,
                    budget.current_usage,
                    budget.limit,
                )

    @property
    def total_records(self) -> int:
        return len(self._records)

    @property
    def total_cost(self) -> float:
        return sum(r.total_cost for r in self._records)
