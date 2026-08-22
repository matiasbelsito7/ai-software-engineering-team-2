"""
Testing pipeline models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TestType(StrEnum):
    """Types of tests."""

    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"


class TestFramework(StrEnum):
    """Testing frameworks."""

    PYTEST = "pytest"
    unittest = "unittest"
    PLAYWRIGHT = "playwright"
    LOCUST = "locust"


class TestStatus(StrEnum):
    """Test execution status."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestFile(BaseModel):
    """A generated test file."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    content: str
    test_type: TestType
    framework: TestFramework = TestFramework.PYTEST
    description: str | None = None


class TestSuite(BaseModel):
    """A collection of test files."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    files: list[TestFile] = Field(default_factory=list)
    test_type: TestType = TestType.UNIT
    framework: TestFramework = TestFramework.PYTEST
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def file_count(self) -> int:
        return len(self.files)


class TestResult(BaseModel):
    """Result of test execution."""

    model_config = ConfigDict(extra="forbid")

    suite_name: str
    status: TestStatus
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration_seconds: float = 0.0
    output: str | None = None
    error_details: list[dict[str, Any]] = Field(default_factory=list)


class TestGenerationRequest(BaseModel):
    """Request for test generation."""

    model_config = ConfigDict(extra="forbid")

    source_files: dict[str, str] = Field(
        ...,
        description="Dict of file_path -> content to generate tests for",
    )
    test_type: TestType = TestType.UNIT
    framework: TestFramework = TestFramework.PYTEST
    coverage_target: float = Field(default=0.8, ge=0.0, le=1.0)
    include_fixtures: bool = True
    include_mocks: bool = True
    context: str | None = None


class TestGenerationResult(BaseModel):
    """Result of test generation."""

    model_config = ConfigDict(extra="forbid")

    suite: TestSuite
    coverage_estimate: float = Field(default=0.0, ge=0.0, le=1.0)
    suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
