"""
Unit tests for the evals subsystem.
"""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003

import pytest

from ai_team.evals.dataset import EvalDataset, TestCase, load_dataset, save_dataset
from ai_team.evals.exceptions import (
    DatasetError,
    MetricError,
    ThresholdError,
)
from ai_team.evals.factory import build_evaluator
from ai_team.evals.metrics import (
    ContextPrecisionMetric,
    ContextRecallMetric,
    CorrectnessMetric,
    FaithfulnessMetric,
    RelevancyMetric,
    get_metric,
)
from ai_team.evals.models import EvalReport, EvalResult, MetricResult
from ai_team.evals.report import generate_json_report, generate_summary, save_json_report

# ======================================================================
# Models
# ======================================================================


class TestMetricResult:
    def test_create(self) -> None:
        r = MetricResult(name="test", score=0.9, passed=True)
        assert r.name == "test"
        assert r.score == 0.9
        assert r.passed is True

    def test_score_bounds(self) -> None:
        with pytest.raises(ValueError):
            MetricResult(name="x", score=1.5, passed=True)

    def test_forbid_extra(self) -> None:
        with pytest.raises(ValueError):
            MetricResult(name="x", score=0.5, passed=True, foo="bar")  # type: ignore[arg-type]


class TestEvalResult:
    def test_defaults(self) -> None:
        r = EvalResult(
            test_case_id="tc-001",
            input="q",
            actual_output="a",
        )
        assert r.passed is False
        assert r.overall_score == 0.0
        assert r.metrics == []


class TestEvalReport:
    def test_defaults(self) -> None:
        report = EvalReport()
        assert report.total_cases == 0
        assert report.average_score == 0.0


# ======================================================================
# Dataset
# ======================================================================


class TestTestCase:
    def test_create(self) -> None:
        tc = TestCase(id="tc-001", input="What is X?", expected_output="X is Y")
        assert tc.id == "tc-001"
        assert tc.context == []


class TestEvalDataset:
    def test_len(self) -> None:
        ds = EvalDataset(
            test_cases=[
                TestCase(id="1", input="a"),
                TestCase(id="2", input="b"),
            ]
        )
        assert len(ds) == 2

    def test_iter(self) -> None:
        ds = EvalDataset(test_cases=[TestCase(id="1", input="a")])
        items = list(ds)
        assert len(items) == 1

    def test_getitem(self) -> None:
        ds = EvalDataset(test_cases=[TestCase(id="1", input="a")])
        assert ds[0].id == "1"


class TestDatasetIO:
    def test_load_and_save(self, tmp_path: Path) -> None:
        dataset = EvalDataset(
            name="test-ds",
            test_cases=[
                TestCase(id="tc-001", input="q1", expected_output="a1"),
                TestCase(id="tc-002", input="q2", context=["doc1"]),
            ],
        )

        path = tmp_path / "dataset.json"
        save_dataset(dataset, path)

        loaded = load_dataset(path)
        assert loaded.name == "test-ds"
        assert len(loaded) == 2
        assert loaded[0].input == "q1"

    def test_load_missing_file(self) -> None:
        with pytest.raises(DatasetError, match="not found"):
            load_dataset("/nonexistent/path.json")

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.json"
        path.write_text("not json {{{", encoding="utf-8")
        with pytest.raises(DatasetError, match="Invalid JSON"):
            load_dataset(path)

    def test_load_list_format(self, tmp_path: Path) -> None:
        path = tmp_path / "list.json"
        path.write_text(
            json.dumps([{"id": "1", "input": "q"}]),
            encoding="utf-8",
        )
        ds = load_dataset(path)
        assert len(ds) == 1
        assert ds[0].id == "1"


# ======================================================================
# Metrics
# ======================================================================


class TestCorrectnessMetric:
    async def test_identical(self) -> None:
        m = CorrectnessMetric()
        r = await m.evaluate(input="q", actual_output="hello world", expected_output="hello world")
        assert r.score == 1.0
        assert r.passed is True

    async def test_different(self) -> None:
        m = CorrectnessMetric()
        r = await m.evaluate(input="q", actual_output="cats", expected_output="dogs")
        assert r.score < 1.0

    async def test_no_expected(self) -> None:
        m = CorrectnessMetric()
        r = await m.evaluate(input="q", actual_output="a")
        assert r.score == 0.5


class TestFaithfulnessMetric:
    async def test_with_context(self) -> None:
        m = FaithfulnessMetric()
        r = await m.evaluate(
            input="q",
            actual_output="the sky is blue",
            context=["the sky is blue and beautiful"],
        )
        assert r.score > 0.0

    async def test_no_context(self) -> None:
        m = FaithfulnessMetric()
        r = await m.evaluate(input="q", actual_output="a")
        assert r.score == 0.5


class TestRelevancyMetric:
    async def test_relevant(self) -> None:
        m = RelevancyMetric()
        r = await m.evaluate(
            input="what is the weather today",
            actual_output="the weather today is sunny",
        )
        assert r.score > 0.0

    async def test_irrelevant(self) -> None:
        m = RelevancyMetric()
        r = await m.evaluate(
            input="what is the weather",
            actual_output="quantum physics is complex",
        )
        assert r.score < 0.5


class TestContextPrecisionMetric:
    async def test_with_context(self) -> None:
        m = ContextPrecisionMetric()
        r = await m.evaluate(
            input="python programming",
            actual_output="answer",
            context=["python is a programming language"],
        )
        assert r.score > 0.0

    async def test_no_context(self) -> None:
        m = ContextPrecisionMetric()
        r = await m.evaluate(input="q", actual_output="a")
        assert r.score == 0.5


class TestContextRecallMetric:
    async def test_with_context(self) -> None:
        m = ContextRecallMetric()
        r = await m.evaluate(
            input="q",
            actual_output="answer",
            expected_output="the answer is 42",
            context=["the answer is 42 and nothing else"],
        )
        assert r.score > 0.0


class TestGetMetric:
    def test_valid(self) -> None:
        m = get_metric("correctness")
        assert isinstance(m, CorrectnessMetric)

    def test_invalid(self) -> None:
        with pytest.raises(MetricError, match="Unknown metric"):
            get_metric("nonexistent")


# ======================================================================
# Runner
# ======================================================================


class TestEvalRunner:
    async def test_evaluate_test_case(self) -> None:
        runner = build_evaluator(metric_names=["correctness"])
        tc = TestCase(
            id="tc-001",
            input="what is 2+2",
            expected_output="4",
        )

        async def fn(q: str) -> str:
            return "4"

        result = await runner.evaluate_test_case(test_case=tc, fn=fn)
        assert isinstance(result, EvalResult)
        assert result.passed is True
        assert len(result.metrics) == 1

    async def test_run_dataset(self) -> None:
        runner = build_evaluator(metric_names=["correctness"])
        dataset = EvalDataset(
            test_cases=[
                TestCase(id="1", input="q1", expected_output="a1"),
                TestCase(id="2", input="q2", expected_output="a2"),
            ]
        )

        async def fn(q: str) -> str:
            return "a1" if q == "q1" else "a2"

        report = await runner.run(dataset=dataset, fn=fn)
        assert isinstance(report, EvalReport)
        assert report.total_cases == 2
        assert report.passed_cases == 2

    async def test_threshold_error(self) -> None:
        from ai_team.infrastructure.config.evaluation import EvaluationSettings

        settings = EvaluationSettings(minimum_score=0.99)
        runner = build_evaluator(settings=settings, metric_names=["correctness"])
        dataset = EvalDataset(
            test_cases=[
                TestCase(id="1", input="q", expected_output="completely different answer"),
            ]
        )

        async def fn(q: str) -> str:
            return "something totally unrelated"

        with pytest.raises(ThresholdError):
            await runner.run(dataset=dataset, fn=fn)

    async def test_metric_error_in_result(self) -> None:
        runner = build_evaluator(metric_names=["correctness"])
        tc = TestCase(id="tc-001", input="q", expected_output="a")

        async def fn(q: str) -> str:
            return "a"

        result = await runner.evaluate_test_case(test_case=tc, fn=fn)
        assert isinstance(result, EvalResult)


# ======================================================================
# Report
# ======================================================================


class TestReport:
    def test_generate_json(self) -> None:
        report = EvalReport(
            total_cases=1,
            passed_cases=1,
            average_score=0.9,
        )
        json_str = generate_json_report(report)
        data = json.loads(json_str)
        assert data["total_cases"] == 1
        assert data["average_score"] == 0.9

    def test_save_json_report(self, tmp_path: Path) -> None:
        report = EvalReport(total_cases=1, passed_cases=1, average_score=0.9)
        path = tmp_path / "report.json"
        save_json_report(report, path)
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["total_cases"] == 1

    def test_generate_summary(self) -> None:
        report = EvalReport(
            total_cases=10,
            passed_cases=8,
            failed_cases=2,
            average_score=0.85,
        )
        summary = generate_summary(report)
        assert summary["pass_rate"] == 0.8
        assert summary["status"] == "FAILED"

    def test_summary_all_pass(self) -> None:
        report = EvalReport(
            total_cases=5,
            passed_cases=5,
            average_score=0.95,
        )
        summary = generate_summary(report)
        assert summary["status"] == "PASSED"
