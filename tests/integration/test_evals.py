"""
Integration tests for the evals subsystem.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.evals.dataset import EvalDataset, TestCase, load_dataset
from ai_team.evals.factory import build_evaluator
from ai_team.evals.models import EvalReport
from ai_team.evals.report import generate_summary, save_json_report
from ai_team.evals.runner import EvalRunner


class TestEvalFactory:
    def test_build_default(self) -> None:
        runner = build_evaluator()
        assert isinstance(runner, EvalRunner)

    def test_build_with_settings(self) -> None:
        from ai_team.infrastructure.config.evaluation import EvaluationSettings

        settings = EvaluationSettings(minimum_score=0.5)
        runner = build_evaluator(settings=settings)
        assert isinstance(runner, EvalRunner)

    def test_build_with_metric_names(self) -> None:
        runner = build_evaluator(metric_names=["correctness", "relevancy"])
        assert isinstance(runner, EvalRunner)


class TestEvalEndToEnd:
    """Full pipeline: dataset -> runner -> report."""

    async def test_perfect_score(self) -> None:
        runner = build_evaluator(metric_names=["correctness"])
        dataset = EvalDataset(
            test_cases=[
                TestCase(id="tc-001", input="What is 2+2?", expected_output="4"),
                TestCase(id="tc-002", input="Capital of France?", expected_output="Paris"),
            ]
        )

        async def perfect_fn(q: str) -> str:
            mapping = {"What is 2+2?": "4", "Capital of France?": "Paris"}
            return mapping.get(q, "unknown")

        report = await runner.run(dataset=dataset, fn=perfect_fn)
        assert isinstance(report, EvalReport)
        assert report.total_cases == 2
        assert report.passed_cases == 2
        assert report.average_score > 0.8

    async def test_with_dataset_file(self, tmp_path: Path) -> None:
        dataset = EvalDataset(
            name="file-test",
            test_cases=[
                TestCase(id="1", input="q1", expected_output="a1"),
            ],
        )

        path = tmp_path / "ds.json"
        save_path = tmp_path / "report.json"

        from ai_team.evals.dataset import save_dataset

        save_dataset(dataset, path)
        loaded = load_dataset(path)

        runner = build_evaluator(metric_names=["correctness"])

        async def fn(q: str) -> str:
            return "a1"

        report = await runner.run(dataset=loaded, fn=fn)
        assert report.total_cases == 1

        save_json_report(report, save_path)
        assert save_path.exists()

    async def test_summary(self) -> None:
        from ai_team.infrastructure.config.evaluation import EvaluationSettings

        settings = EvaluationSettings(minimum_score=0.3)
        runner = build_evaluator(
            settings=settings,
            metric_names=["correctness", "relevancy"],
        )
        dataset = EvalDataset(
            test_cases=[
                TestCase(
                    id="1",
                    input="What is Python?",
                    expected_output="Python is a programming language",
                ),
            ]
        )

        async def fn(q: str) -> str:
            return "Python is a programming language"

        report = await runner.run(dataset=dataset, fn=fn)
        summary = generate_summary(report)
        assert "pass_rate" in summary
        assert "status" in summary
