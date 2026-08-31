"""
Admin router.

Provides admin-only endpoints for platform metrics and user management.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Depends

from ai_team.app.api.dependencies import get_current_admin
from ai_team.domain.schemas.auth import UserResponse
from ai_team.infrastructure.database.session import get_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/metrics",
    summary="Get platform metrics",
)
async def get_admin_metrics(
    current_user: UserResponse = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """
    Get aggregated platform metrics.

    Requires admin role.
    """
    from sqlalchemy import func, select

    from ai_team.domain.models.project import Project
    from ai_team.domain.models.user import User

    # Total users
    user_count_result = await session.execute(select(func.count(User.id)))
    total_users = user_count_result.scalar() or 0

    # Active users
    active_users_result = await session.execute(
        select(func.count(User.id)).where(User.is_active.is_(True))
    )
    active_users = active_users_result.scalar() or 0

    # Total projects
    project_count_result = await session.execute(select(func.count(Project.id)))
    total_projects = project_count_result.scalar() or 0

    # Projects by status
    status_result = await session.execute(
        select(Project.status, func.count(Project.id)).group_by(Project.status)
    )
    projects_by_status = {row[0]: row[1] for row in status_result.all()}

    # Total tokens used
    tokens_result = await session.execute(
        select(func.coalesce(func.sum(Project.tokens_used), 0))
    )
    total_tokens = tokens_result.scalar() or 0

    # Projects by tier
    tier_result = await session.execute(
        select(Project.tier, func.count(Project.id)).group_by(Project.tier)
    )
    projects_by_tier = {row[0]: row[1] for row in tier_result.all()}

    # Total iterations
    iter_result = await session.execute(
        select(func.coalesce(func.sum(Project.iterations_used), 0))
    )
    total_iterations = iter_result.scalar() or 0

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_projects": total_projects,
        "projects_by_status": projects_by_status,
        "projects_by_tier": projects_by_tier,
        "total_tokens_used": total_tokens,
        "total_iterations": total_iterations,
    }


@router.get(
    "/users",
    summary="List all users",
)
async def list_users(
    current_user: UserResponse = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 50,
) -> dict[str, Any]:
    """
    List all users with pagination.

    Requires admin role.
    """
    from sqlalchemy import func, select

    from ai_team.domain.models.user import User

    count_result = await session.execute(select(func.count(User.id)))
    total = count_result.scalar() or 0

    result = await session.execute(
        select(User).offset(offset).limit(limit).order_by(User.created_at.desc())
    )
    users = result.scalars().all()

    return {
        "users": [
            {
                "id": str(u.id),
                "email": u.email,
                "role": u.role,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "total": total,
        "offset": offset,
        "limit": limit,
    }
