"""
Deployment automation API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PipelineFileSchema(BaseModel):
    """Generated pipeline file schema."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    content: str
    platform: str
    description: str | None = None


class DeploymentPlanSchema(BaseModel):
    """Deployment plan schema."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    platform: str
    files: list[PipelineFileSchema]
    instructions: str | None = None


class DeploymentRequestSchema(BaseModel):
    """Request for deployment pipeline generation."""

    model_config = ConfigDict(extra="forbid")

    project_name: str
    platform: str = "github_actions"
    language: str = "python"
    language_version: str = "3.12"
    include_docker: bool = True
    include_tests: bool = True
    include_linting: bool = True
    include_security: bool = True
    environments: list[str] | None = None
    context: str | None = None
