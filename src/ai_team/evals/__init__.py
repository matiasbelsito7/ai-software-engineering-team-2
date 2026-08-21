"""
Evaluation subsystem.
"""

from ai_team.evals.dataset import EvalDataset, TestCase, load_dataset, save_dataset
from ai_team.evals.exceptions import (
    DatasetError,
    EvalError,
    MetricError,
    ReportError,
    ThresholdError,
)
from ai_team.evals.factory import build_evaluator
from ai_team.evals.metrics import (
    BaseMetric,
    ContextPrecisionMetric,
    ContextRecallMetric,
    CorrectnessMetric,
    FaithfulnessMetric,
    RelevancyMetric,
    get_metric,
)
from ai_team.evals.models import EvalReport, EvalResult, MetricResult
from ai_team.evals.report import (
    generate_json_report,
    generate_summary,
    save_json_report,
)
from ai_team.evals.runner import EvalRunner

__all__ = [
    "BaseMetric",
    "ContextPrecisionMetric",
    "ContextRecallMetric",
    "CorrectnessMetric",
    "DatasetError",
    "EvalDataset",
    "EvalError",
    "EvalReport",
    "EvalResult",
    "EvalRunner",
    "FaithfulnessMetric",
    "MetricError",
    "MetricResult",
    "RelevancyMetric",
    "ReportError",
    "TestCase",
    "ThresholdError",
    "build_evaluator",
    "generate_json_report",
    "generate_summary",
    "get_metric",
    "load_dataset",
    "save_dataset",
    "save_json_report",
]
