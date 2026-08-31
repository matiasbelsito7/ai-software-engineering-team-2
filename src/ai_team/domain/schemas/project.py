"""
Project API schemas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID


# =====================================================================
# Request schemas
# =====================================================================


class CreateProjectRequest(BaseModel):
    """Request body for POST /projects."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Project name.",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural language description of the app to generate.",
    )
    tier: str = Field(
        default="free",
        description="Subscription tier: free, starter, pro, business.",
    )


class UpdateProjectRequest(BaseModel):
    """Request body for PUT /projects/{project_id}."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New project name.",
    )


# =====================================================================
# Response schemas
# =====================================================================


class TierInfo(BaseModel):
    """Tier information response."""

    model_config = ConfigDict(extra="forbid")

    name: str
    display_name: str
    price_monthly: float
    tokens_per_project: int
    max_iterations: int
    max_projects: int
    retention_days: int
    can_download_code: bool


class ProjectResponse(BaseModel):
    """Project response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    tier: str
    tokens_used: int
    iterations_used: int
    status: str
    files_path: str | None = None
    created_at: datetime
    updated_at: datetime
    expires_at: datetime

    @classmethod
    def from_project(cls, project: Any) -> ProjectResponse:
        """Create response from Project ORM model."""
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            tier=project.tier,
            tokens_used=project.tokens_used,
            iterations_used=project.iterations_used,
            status=project.status,
            files_path=project.files_path,
            created_at=project.created_at,
            updated_at=project.updated_at,
            expires_at=project.expires_at,
        )


class ProjectListResponse(BaseModel):
    """Paginated project list response."""

    model_config = ConfigDict(extra="forbid")

    projects: list[ProjectResponse] = Field(
        default_factory=list,
    )
    total: int = 0
    offset: int = 0
    limit: int = 0


class ProjectStatsResponse(BaseModel):
    """Project usage stats for the current user."""

    model_config = ConfigDict(extra="forbid")

    total_projects: int = 0
    projects_by_status: dict[str, int] = Field(
        default_factory=dict,
    )
    total_tokens_used: int = 0
    current_tier: str = "free"
    projects_remaining: int | None = None  # None = unlimited
