"""
Deployment automation models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CICDPlatform(StrEnum):
    """CI/CD platforms."""

    GITHUB_ACTIONS = "github_actions"
    GITLAB_CI = "gitlab_ci"
    JENKINS = "jenkins"
    CIRCLECI = "circleci"
    AZURE_DEVOPS = "azure_devops"


class DeploymentEnvironment(StrEnum):
    """Deployment environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class PipelineStage(StrEnum):
    """Pipeline stages."""

    BUILD = "build"
    TEST = "test"
    LINT = "lint"
    SECURITY = "security"
    DEPLOY = "deploy"
    NOTIFY = "notify"


class PipelineStep(BaseModel):
    """A single step in a pipeline."""

    model_config = ConfigDict(extra="forbid")

    name: str
    stage: PipelineStage
    command: str | None = None
    uses: str | None = None
    with_params: dict[str, Any] | None = None
    env: dict[str, str] | None = None
    if_condition: str | None = None
    needs: list[str] | None = None


class PipelineConfig(BaseModel):
    """CI/CD pipeline configuration."""

    model_config = ConfigDict(extra="forbid")

    platform: CICDPlatform
    project_name: str
    language: str = "python"
    language_version: str = "3.12"
    environments: list[DeploymentEnvironment] = Field(
        default_factory=lambda: [DeploymentEnvironment.DEVELOPMENT, DeploymentEnvironment.STAGING]
    )
    steps: list[PipelineStep] = Field(default_factory=list)
    variables: dict[str, str] = Field(default_factory=dict)
    secrets: list[str] | None = None
    triggers: list[str] | None = None


class PipelineFile(BaseModel):
    """A generated pipeline file."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    content: str
    platform: CICDPlatform
    description: str | None = None


class DeploymentPlan(BaseModel):
    """Complete deployment plan."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    platform: CICDPlatform
    files: list[PipelineFile] = Field(default_factory=list)
    instructions: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DeploymentRequest(BaseModel):
    """Request for deployment pipeline generation."""

    model_config = ConfigDict(extra="forbid")

    project_name: str
    platform: CICDPlatform = CICDPlatform.GITHUB_ACTIONS
    language: str = "python"
    language_version: str = "3.12"
    include_docker: bool = True
    include_tests: bool = True
    include_linting: bool = True
    include_security: bool = True
    environments: list[DeploymentEnvironment] | None = None
    custom_steps: list[dict[str, Any]] | None = None
    context: str | None = None
