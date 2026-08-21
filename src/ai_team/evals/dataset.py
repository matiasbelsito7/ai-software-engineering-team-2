"""
Dataset loading for evaluations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ai_team.evals.exceptions import DatasetError


class TestCase(BaseModel):
    """
    A single evaluation test case.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    id: str

    input: str

    expected_output: str | None = None

    context: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvalDataset(BaseModel):
    """
    Collection of test cases for evaluation.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str = "default"

    test_cases: list[TestCase] = Field(
        default_factory=list,
    )

    def __len__(self) -> int:
        return len(self.test_cases)

    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(self.test_cases)

    def __getitem__(self, index: int) -> TestCase:
        return self.test_cases[index]


def load_dataset(path: str | Path) -> EvalDataset:
    """
    Load an evaluation dataset from a JSON file.

    Expected format::

        {
            "name": "my-dataset",
            "test_cases": [
                {
                    "id": "tc-001",
                    "input": "What is X?",
                    "expected_output": "X is ...",
                    "context": ["doc1", "doc2"]
                }
            ]
        }
    """

    file_path = Path(path)

    if not file_path.exists():
        raise DatasetError(f"Dataset file not found: {file_path}")

    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DatasetError(
            f"Invalid JSON in dataset file: {file_path}",
        ) from exc

    if isinstance(raw, list):
        raw = {"name": file_path.stem, "test_cases": raw}

    try:
        return EvalDataset(**raw)
    except Exception as exc:
        raise DatasetError(
            f"Failed to parse dataset: {exc}",
        ) from exc


def save_dataset(dataset: EvalDataset, path: str | Path) -> None:
    """
    Save an evaluation dataset to a JSON file.
    """

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "name": dataset.name,
        "test_cases": [tc.model_dump() for tc in dataset.test_cases],
    }

    file_path.write_text(
        json.dumps(data, indent=2, default=str),
        encoding="utf-8",
    )
