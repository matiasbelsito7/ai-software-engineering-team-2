"""
Project service.

Handles project CRUD, tier validation, and usage tracking.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import func, select

from ai_team.domain.models.project import Project
from ai_team.domain.models.tier import ALL_TIER_NAMES, get_tier

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ProjectError(Exception):
    """Base project error."""

    def __init__(self, message: str, code: str = "PROJECT_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class ProjectNotFoundError(ProjectError):
    """Project not found."""

    def __init__(self, project_id: str) -> None:
        super().__init__(f"Project not found: {project_id}", "PROJECT_NOT_FOUND")


class InvalidTierError(ProjectError):
    """Invalid tier name."""

    def __init__(self, tier: str) -> None:
        super().__init__(
            f"Invalid tier: {tier}. Must be one of {ALL_TIER_NAMES}",
            "INVALID_TIER",
        )


class ProjectLimitExceededError(ProjectError):
    """User has reached project limit for their tier."""

    def __init__(self, tier: str, limit: int) -> None:
        super().__init__(
            f"Project limit reached for {tier} tier (max {limit}). "
            "Upgrade your plan to create more projects.",
            "PROJECT_LIMIT_EXCEEDED",
        )


class BudgetExhaustedError(ProjectError):
    """Token budget for this project is exhausted."""

    def __init__(self, tokens_used: int, budget: int) -> None:
        super().__init__(
            f"Token budget exhausted ({tokens_used}/{budget}). " "Upgrade your plan to continue.",
            "BUDGET_EXHAUSTED",
        )


class ProjectService:
    """Project management service."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -----------------------------------------------------------------
    # CRUD operations
    # -----------------------------------------------------------------

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        name: str,
        description: str,
        tier: str,
    ) -> Project:
        """Create a new project."""
        # Validate tier
        tier_config = get_tier(tier)

        # Check project limit
        await self._check_project_limit(user_id, tier, tier_config.max_projects)

        # Create project
        project = Project.create(
            user_id=user_id,
            name=name,
            description=description,
            tier=tier,
            retention_days=tier_config.retention_days,
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get(self, project_id: str, user_id: uuid.UUID) -> Project:
        """Get a project by ID (must belong to user)."""
        try:
            pid = uuid.UUID(project_id)
        except ValueError as e:
            raise ProjectNotFoundError(project_id) from e

        result = await self.session.execute(
            select(Project).where(
                Project.id == pid,
                Project.user_id == user_id,
            ),
        )
        project = result.scalar_one_or_none()
        if project is None:
            raise ProjectNotFoundError(project_id)
        return project

    async def list_by_user(
        self,
        user_id: uuid.UUID,
        *,
        offset: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> tuple[list[Project], int]:
        """List projects for a user with pagination."""
        query = select(Project).where(Project.user_id == user_id)

        if status:
            query = query.where(Project.status == status)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(Project.created_at.desc())
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        projects = list(result.scalars().all())

        return projects, total

    async def update(
        self,
        project_id: str,
        user_id: uuid.UUID,
        *,
        name: str | None = None,
        files_path: str | None = None,
    ) -> Project:
        """Update a project."""
        project = await self.get(project_id, user_id)

        if name is not None:
            project.name = name

        if files_path is not None:
            project.files_path = files_path

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project_id: str, user_id: uuid.UUID) -> None:
        """Delete a project."""
        project = await self.get(project_id, user_id)
        await self.session.delete(project)
        await self.session.commit()

    # -----------------------------------------------------------------
    # Usage tracking
    # -----------------------------------------------------------------

    async def record_tokens(
        self,
        project_id: str,
        user_id: uuid.UUID,
        tokens: int,
    ) -> Project:
        """Record token usage for a project."""
        project = await self.get(project_id, user_id)
        tier_config = get_tier(project.tier)

        project.tokens_used += tokens
        if project.tokens_used > tier_config.tokens_per_project:
            await self.session.rollback()
            raise BudgetExhaustedError(
                project.tokens_used,
                tier_config.tokens_per_project,
            ) from None

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def increment_iteration(
        self,
        project_id: str,
        user_id: uuid.UUID,
    ) -> Project:
        """Increment iteration count for a project."""
        project = await self.get(project_id, user_id)
        tier_config = get_tier(project.tier)

        project.iterations_used += 1
        if project.iterations_used > tier_config.max_iterations:
            await self.session.rollback()
            raise BudgetExhaustedError(
                project.iterations_used,
                tier_config.max_iterations,
            ) from None

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update_status(
        self,
        project_id: str,
        user_id: uuid.UUID,
        status: str,
    ) -> Project:
        """Update project status."""
        project = await self.get(project_id, user_id)
        project.status = status
        await self.session.commit()
        await self.session.refresh(project)
        return project

    # -----------------------------------------------------------------
    # Stats
    # -----------------------------------------------------------------

    async def get_user_stats(self, user_id: uuid.UUID) -> dict[str, Any]:
        """Get project stats for a user."""
        # Total projects
        count_result = await self.session.execute(
            select(func.count()).where(Project.user_id == user_id),
        )
        total_projects = count_result.scalar() or 0

        # Projects by status
        status_result = await self.session.execute(
            select(Project.status, func.count())
            .where(Project.user_id == user_id)
            .group_by(Project.status),
        )
        projects_by_status = {row[0]: row[1] for row in status_result.all()}

        # Total tokens used
        tokens_result = await self.session.execute(
            select(func.coalesce(func.sum(Project.tokens_used), 0)).where(
                Project.user_id == user_id,
            ),
        )
        total_tokens = tokens_result.scalar() or 0

        return {
            "total_projects": total_projects,
            "projects_by_status": projects_by_status,
            "total_tokens_used": total_tokens,
        }

    # -----------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------

    async def _check_project_limit(
        self,
        user_id: uuid.UUID,
        tier: str,
        max_projects: int,
    ) -> None:
        """Check if user has reached project limit."""
        if max_projects == -1:
            return  # unlimited

        count_result = await self.session.execute(
            select(func.count()).where(Project.user_id == user_id),
        )
        current_count = count_result.scalar() or 0

        if current_count >= max_projects:
            raise ProjectLimitExceededError(tier, max_projects)
