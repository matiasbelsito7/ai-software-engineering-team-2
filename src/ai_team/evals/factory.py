"""
Evaluation factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.evals.metrics import BaseMetric, get_metric
from ai_team.evals.runner import EvalRunner

if TYPE_CHECKING:
    from ai_team.infrastructure.config.evaluation import (
        EvaluationSettings,
    )


def build_evaluator(
    *,
    settings: EvaluationSettings | None = None,
    metric_names: list[str] | None = None,
) -> EvalRunner:
    """
    Build the evaluation subsystem.

    If metric_names is provided, only those metrics are used.
    Otherwise, metrics are selected based on settings.
    """

    metrics: list[BaseMetric] | None = None

    if metric_names is not None:
        metrics = [get_metric(n) for n in metric_names]

    return EvalRunner(
        settings=settings,
        metrics=metrics,
    )
