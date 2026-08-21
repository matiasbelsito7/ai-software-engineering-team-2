"""
Evaluation runner.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from ai_team.evals.dataset import EvalDataset, TestCase  # noqa: TC001
from ai_team.evals.exceptions import ThresholdError
from ai_team.evals.metrics import BaseMetric, get_metric
from ai_team.evals.models import EvalReport, EvalResult, MetricResult

if TYPE_CHECKING:
    from ai_team.infrastructure.config.evaluation import (
        EvaluationSettings,
    )


# Type alias for the function under evaluation
EvaluableFn = Callable[[str], Awaitable[str]]


class EvalRunner:
    """
    Orchestrates evaluation runs.
    """

    def __init__(
        self,
        *,
        settings: EvaluationSettings | None = None,
        metrics: list[BaseMetric] | None = None,
    ) -> None:
        self._settings = settings
        self._metrics = metrics or self._default_metrics()

    # ------------------------------------------------------------------
    # Default metrics from settings
    # ------------------------------------------------------------------

    def _default_metrics(self) -> list[BaseMetric]:
        names: list[str] = []

        if self._settings is None:
            return [
                get_metric("correctness"),
                get_metric("relevancy"),
            ]

        if self._settings.evaluate_correctness:
            names.append("correctness")
        if self._settings.evaluate_faithfulness:
            names.append("faithfulness")
        if self._settings.evaluate_relevancy:
            names.append("relevancy")
        if self._settings.evaluate_context_precision:
            names.append("context_precision")
        if self._settings.evaluate_context_recall:
            names.append("context_recall")

        if not names:
            names = ["correctness", "relevancy"]

        return [get_metric(n) for n in names]

    # ------------------------------------------------------------------
    # Single test case
    # ------------------------------------------------------------------

    async def evaluate_test_case(
        self,
        *,
        test_case: TestCase,
        fn: EvaluableFn,
    ) -> EvalResult:
        """
        Evaluate a single test case.
        """

        actual_output = await fn(test_case.input)

        metric_results: list[MetricResult] = []
        for metric in self._metrics:
            try:
                result = await metric.evaluate(
                    input=test_case.input,
                    actual_output=actual_output,
                    expected_output=test_case.expected_output,
                    context=test_case.context or None,
                )
                metric_results.append(result)
            except Exception as exc:
                metric_results.append(
                    MetricResult(
                        name=metric.name,
                        score=0.0,
                        passed=False,
                        details=f"Metric error: {exc}",
                    )
                )

        scores = [m.score for m in metric_results]
        overall = sum(scores) / len(scores) if scores else 0.0

        threshold = self._settings.minimum_score if self._settings else 0.8
        passed = overall >= threshold

        return EvalResult(
            test_case_id=test_case.id,
            input=test_case.input,
            actual_output=actual_output,
            expected_output=test_case.expected_output,
            context=test_case.context,
            metrics=metric_results,
            overall_score=round(overall, 4),
            passed=passed,
        )

    # ------------------------------------------------------------------
    # Full dataset
    # ------------------------------------------------------------------

    async def run(
        self,
        *,
        dataset: EvalDataset,
        fn: EvaluableFn,
    ) -> EvalReport:
        """
        Run evaluation on an entire dataset.
        """

        start = time.monotonic()
        results: list[EvalResult] = []
        threshold = self._settings.minimum_score if self._settings else 0.8

        for test_case in dataset:
            result = await self.evaluate_test_case(
                test_case=test_case,
                fn=fn,
            )
            results.append(result)

            if not result.passed and self._settings and self._settings.fail_fast:
                break

        elapsed = time.monotonic() - start

        passed_count = sum(1 for r in results if r.passed)
        failed_count = len(results) - passed_count
        avg_score = sum(r.overall_score for r in results) / len(results) if results else 0.0

        # Compute per-metric averages
        metric_sums: dict[str, float] = {}
        metric_counts: dict[str, int] = {}
        for r in results:
            for m in r.metrics:
                metric_sums[m.name] = metric_sums.get(m.name, 0.0) + m.score
                metric_counts[m.name] = metric_counts.get(m.name, 0) + 1

        metric_avgs = {
            name: round(metric_sums[name] / metric_counts[name], 4) for name in metric_sums
        }

        report = EvalReport(
            results=results,
            total_cases=len(results),
            passed_cases=passed_count,
            failed_cases=failed_count,
            average_score=round(avg_score, 4),
            metric_averages=metric_avgs,
            threshold=threshold,
            duration_seconds=round(elapsed, 4),
        )

        # Validate thresholds
        if report.average_score < threshold:
            raise ThresholdError(
                f"Average score {report.average_score:.4f} is below "
                f"threshold {threshold:.4f}. "
                f"Passed: {passed_count}/{len(results)}",
            )

        return report
