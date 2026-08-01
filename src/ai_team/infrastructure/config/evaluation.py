```python
"""
Evaluation configuration.

Defines the configuration for the evaluation framework.

This module contains configuration only.

Implementations belong to:

    evals/
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EvaluationSettings(BaseSettings):
    """
    Evaluation framework configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="EVAL_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Global
    ###########################################################################

    enabled: bool = Field(
        default=True,
        description="Enable evaluation framework.",
    )

    framework: str = Field(
        default="deepeval",
        description="Evaluation framework.",
    )

    ###########################################################################
    # Dataset
    ###########################################################################

    dataset_path: str = Field(
        default="datasets",
        description="Directory containing evaluation datasets.",
    )

    benchmark_path: str = Field(
        default="benchmarks",
        description="Directory containing benchmark definitions.",
    )

    ###########################################################################
    # LLM Judge
    ###########################################################################

    enable_llm_judge: bool = Field(
        default=True,
        description="Enable LLM-as-a-Judge.",
    )

    judge_model: str = Field(
        default="anthropic/claude-sonnet-4",
        description="Judge model identifier.",
    )

    ###########################################################################
    # Metrics
    ###########################################################################

    evaluate_correctness: bool = Field(
        default=True,
        description="Evaluate answer correctness.",
    )

    evaluate_faithfulness: bool = Field(
        default=True,
        description="Evaluate factual faithfulness.",
    )

    evaluate_relevancy: bool = Field(
        default=True,
        description="Evaluate response relevance.",
    )

    evaluate_context_precision: bool = Field(
        default=True,
        description="Evaluate retrieved context precision.",
    )

    evaluate_context_recall: bool = Field(
        default=True,
        description="Evaluate retrieved context recall.",
    )

    ###########################################################################
    # Thresholds
    ###########################################################################

    minimum_score: float = Field(
        default=0.80,
        ge=0.0,
        le=1.0,
        description="Minimum acceptable evaluation score.",
    )

    fail_fast: bool = Field(
        default=False,
        description="Stop execution after the first failed evaluation.",
    )

    ###########################################################################
    # Reports
    ###########################################################################

    save_reports: bool = Field(
        default=True,
        description="Persist evaluation reports.",
    )

    reports_directory: str = Field(
        default="reports/evaluations",
        description="Evaluation reports directory.",
    )

    export_json: bool = Field(
        default=True,
        description="Export JSON reports.",
    )

    export_html: bool = Field(
        default=True,
        description="Export HTML reports.",
    )

    ###########################################################################
    # Regression
    ###########################################################################

    compare_with_previous: bool = Field(
        default=True,
        description="Compare results with previous executions.",
    )

    keep_history: bool = Field(
        default=True,
        description="Store evaluation history.",
    )
```
