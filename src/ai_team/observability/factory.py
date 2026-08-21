"""
Observability module factory.
"""

from __future__ import annotations

from ai_team.observability.costs import CostTracker
from ai_team.observability.manager import ObservationManager
from ai_team.observability.telemetry.logging import LoggingManager
from ai_team.observability.telemetry.metrics import MetricsManager
from ai_team.observability.telemetry.tracing import TracingManager
from ai_team.observability.token_usage import TokenUsageTracker


def build_observability() -> ObservationManager:
    """
    Build the observability subsystem.
    """

    tracing = TracingManager()

    metrics = MetricsManager()

    logging = LoggingManager()

    token_usage = TokenUsageTracker()

    costs = CostTracker()

    return ObservationManager(
        tracing=tracing,
        metrics=metrics,
        logging=logging,
        token_usage=token_usage,
        costs=costs,
    )
