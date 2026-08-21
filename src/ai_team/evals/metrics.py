"""
Evaluation metrics.

Each metric implements a simple heuristic scoring approach.
Future implementation: integrate with deepeval for LLM-as-a-Judge.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from ai_team.evals.exceptions import MetricError
from ai_team.evals.models import MetricResult


def _tokenize(text: str) -> list[str]:
    """Simple word tokenization."""
    return [w.lower() for w in re.findall(r"\w+", text) if len(w) > 1]


def _jaccard_similarity(a: list[str], b: list[str]) -> float:
    """Jaccard similarity between two token lists."""
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _overlap_coefficient(a: list[str], b: list[str]) -> float:
    """Overlap coefficient (intersection / min size)."""
    set_a, set_b = set(a), set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / min(len(set_a), len(set_b))


class BaseMetric(ABC):
    """
    Abstract base for evaluation metrics.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable metric name."""

    @abstractmethod
    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        """Compute the metric score."""


class CorrectnessMetric(BaseMetric):
    """
    Evaluates whether the actual output matches the expected output.

    Uses token overlap and exact match heuristics.
    """

    @property
    def name(self) -> str:
        return "correctness"

    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        if expected_output is None:
            return MetricResult(
                name=self.name,
                score=0.5,
                passed=False,
                details="No expected output provided; cannot evaluate correctness.",
            )

        actual_tokens = _tokenize(actual_output)
        expected_tokens = _tokenize(expected_output)

        jaccard = _jaccard_similarity(actual_tokens, expected_tokens)
        overlap = _overlap_coefficient(actual_tokens, expected_tokens)

        if actual_output.strip().lower() == expected_output.strip().lower():
            score = 1.0
        else:
            score = 0.5 * jaccard + 0.5 * overlap

        return MetricResult(
            name=self.name,
            score=round(score, 4),
            passed=score >= 0.5,
            details=f"Jaccard={jaccard:.4f}, Overlap={overlap:.4f}",
        )


class FaithfulnessMetric(BaseMetric):
    """
    Evaluates whether the actual output is faithful to the provided context.

    Uses context overlap heuristics.
    """

    @property
    def name(self) -> str:
        return "faithfulness"

    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        if not context:
            return MetricResult(
                name=self.name,
                score=0.5,
                passed=True,
                details="No context provided; skipping faithfulness check.",
            )

        output_tokens = _tokenize(actual_output)
        context_tokens: list[str] = []
        for doc in context:
            context_tokens.extend(_tokenize(doc))

        overlap = _overlap_coefficient(output_tokens, context_tokens)

        return MetricResult(
            name=self.name,
            score=round(overlap, 4),
            passed=overlap >= 0.3,
            details=f"Context overlap={overlap:.4f}",
        )


class RelevancyMetric(BaseMetric):
    """
    Evaluates whether the actual output is relevant to the input query.

    Uses token overlap between input and output.
    """

    @property
    def name(self) -> str:
        return "relevancy"

    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        input_tokens = _tokenize(input)
        output_tokens = _tokenize(actual_output)

        overlap = _overlap_coefficient(input_tokens, output_tokens)
        jaccard = _jaccard_similarity(input_tokens, output_tokens)

        score = 0.6 * overlap + 0.4 * jaccard

        return MetricResult(
            name=self.name,
            score=round(score, 4),
            passed=score >= 0.3,
            details=f"Input-output overlap={overlap:.4f}, Jaccard={jaccard:.4f}",
        )


class ContextPrecisionMetric(BaseMetric):
    """
    Evaluates precision of retrieved context w.r.t. the input.

    Measures how much of the context is relevant to the query.
    """

    @property
    def name(self) -> str:
        return "context_precision"

    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        if not context:
            return MetricResult(
                name=self.name,
                score=0.5,
                passed=True,
                details="No context provided; defaulting to neutral score.",
            )

        input_tokens = _tokenize(input)
        precisions: list[float] = []
        for doc in context:
            doc_tokens = _tokenize(doc)
            precisions.append(_overlap_coefficient(input_tokens, doc_tokens))

        avg_precision = sum(precisions) / len(precisions) if precisions else 0.0

        return MetricResult(
            name=self.name,
            score=round(avg_precision, 4),
            passed=avg_precision >= 0.2,
            details=f"Avg context precision={avg_precision:.4f} over {len(precisions)} docs",
        )


class ContextRecallMetric(BaseMetric):
    """
    Evaluates recall of retrieved context w.r.t. the expected output.

    Measures how much of the expected answer is covered by the context.
    """

    @property
    def name(self) -> str:
        return "context_recall"

    async def evaluate(
        self,
        *,
        input: str,
        actual_output: str,
        expected_output: str | None = None,
        context: list[str] | None = None,
    ) -> MetricResult:
        if not context:
            return MetricResult(
                name=self.name,
                score=0.5,
                passed=True,
                details="No context provided; defaulting to neutral score.",
            )

        reference = expected_output or actual_output
        ref_tokens = _tokenize(reference)
        context_tokens: list[str] = []
        for doc in context:
            context_tokens.extend(_tokenize(doc))

        recall = _overlap_coefficient(ref_tokens, context_tokens)

        return MetricResult(
            name=self.name,
            score=round(recall, 4),
            passed=recall >= 0.3,
            details=f"Context recall={recall:.4f}",
        )


# ======================================================================
# Metric registry
# ======================================================================


METRIC_REGISTRY: dict[str, type[BaseMetric]] = {
    "correctness": CorrectnessMetric,
    "faithfulness": FaithfulnessMetric,
    "relevancy": RelevancyMetric,
    "context_precision": ContextPrecisionMetric,
    "context_recall": ContextRecallMetric,
}


def get_metric(name: str) -> BaseMetric:
    """Instantiate a metric by name."""
    cls = METRIC_REGISTRY.get(name)
    if cls is None:
        available = ", ".join(sorted(METRIC_REGISTRY))
        raise MetricError(
            f"Unknown metric {name!r}. Available: {available}",
        )
    return cls()
