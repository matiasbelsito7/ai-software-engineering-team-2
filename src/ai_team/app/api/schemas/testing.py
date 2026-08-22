"""
Testing pipeline API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TestFileSchema(BaseModel):
    """Generated test file schema."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    content: str
    test_type: str
    framework: str
    description: str | None = None


class TestSuiteSchema(BaseModel):
    """Test suite schema."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    files: list[TestFileSchema]
    test_type: str
    framework: str
    file_count: int


class TestGenerationRequestSchema(BaseModel):
    """Request for test generation."""

    model_config = ConfigDict(extra="forbid")

    source_files: dict[str, str] = Field(
        ...,
        description="Dict of file_path -> content to generate tests for",
    )
    test_type: str = "unit"
    framework: str = "pytest"
    coverage_target: float = Field(default=0.8, ge=0.0, le=1.0)
    include_fixtures: bool = True
    include_mocks: bool = True
    context: str | None = None


class TestGenerationResultSchema(BaseModel):
    """Result of test generation."""

    model_config = ConfigDict(extra="forbid")

    suite: TestSuiteSchema
    coverage_estimate: float
    suggestions: list[str]
    warnings: list[str]
