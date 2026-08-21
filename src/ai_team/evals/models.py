"""
Evaluation models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class MetricResult(BaseModel):
    """
    Result of a single metric evaluation.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    score: float = Field(
        ge=0.0,
        le=1.0,
    )

    passed: bool

    details: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvalResult(BaseModel):
    """
    Result of evaluating a single test case.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    test_case_id: str

    input: str

    actual_output: str

    expected_output: str | None = None

    context: list[str] = Field(
        default_factory=list,
    )

    metrics: list[MetricResult] = Field(
        default_factory=list,
    )

    overall_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    passed: bool = False

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )


class EvalReport(BaseModel):
    """
    Aggregated report of an evaluation run.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    results: list[EvalResult] = Field(
        default_factory=list,
    )

    total_cases: int = 0

    passed_cases: int = 0

    failed_cases: int = 0

    average_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    metric_averages: dict[str, float] = Field(
        default_factory=dict,
    )

    threshold: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    duration_seconds: float = 0.0
