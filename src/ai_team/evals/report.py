"""
Report generation for evaluations.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ai_team.evals.exceptions import ReportError

if TYPE_CHECKING:
    from ai_team.evals.models import EvalReport


def generate_json_report(report: EvalReport) -> str:
    """
    Serialize an EvalReport to a JSON string.
    """

    try:
        return report.model_dump_json(indent=2)
    except Exception as exc:
        raise ReportError(
            f"Failed to generate JSON report: {exc}",
        ) from exc


def save_json_report(
    report: EvalReport,
    path: str | Path | None = None,
) -> Path:
    """
    Save an EvalReport as a JSON file.
    """

    if path is None:
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        path = Path("reports/evaluations") / f"eval_report_{timestamp}.json"

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        content = generate_json_report(report)
        file_path.write_text(content, encoding="utf-8")
    except ReportError:
        raise
    except Exception as exc:
        raise ReportError(
            f"Failed to save JSON report: {exc}",
        ) from exc

    return file_path


def generate_summary(report: EvalReport) -> dict[str, Any]:
    """
    Generate a human-readable summary dict from a report.
    """

    return {
        "total_cases": report.total_cases,
        "passed_cases": report.passed_cases,
        "failed_cases": report.failed_cases,
        "pass_rate": (
            round(report.passed_cases / report.total_cases, 4) if report.total_cases > 0 else 0.0
        ),
        "average_score": report.average_score,
        "metric_averages": report.metric_averages,
        "threshold": report.threshold,
        "duration_seconds": report.duration_seconds,
        "status": "PASSED" if report.failed_cases == 0 else "FAILED",
    }
