"""
Evaluation exceptions.
"""

from __future__ import annotations


class EvalError(Exception):
    """
    Base exception for the evaluation subsystem.
    """


class DatasetError(EvalError):
    """
    Raised when dataset loading or parsing fails.
    """


class MetricError(EvalError):
    """
    Raised when metric computation fails.
    """


class ReportError(EvalError):
    """
    Raised when report generation fails.
    """


class ThresholdError(EvalError):
    """
    Raised when a metric score is below the minimum threshold.
    """
