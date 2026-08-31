"""
Projects router.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse, Response

from ai_team.app.api.schemas.tasks import ErrorResponse
from ai_team.domain.models.tier import TIERS, get_tier
from ai_team.domain.schemas.project import (
    CreateProjectRequest,
    ProjectListResponse,
    ProjectResponse,
    ProjectStatsResponse,
    TierInfo,
    UpdateProjectRequest,
)
from ai_team.domain.services.auth_service import AuthService, InvalidTokenError
from ai_team.domain.services.project_service import (
    ProjectError,
    ProjectService,
)
from ai_team.infrastructure.database.session import get_session

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

    from ai_team.domain.schemas.auth import UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["projects"])


# ---------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------


async def get_project_service(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[ProjectService, None]:
    """Yield a ProjectService instance."""
    yield ProjectService(session)


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Extract and validate the current user from JWT."""
    if not authorization.startswith("Bearer "):
        raise InvalidTokenError("Invalid authorization header format")

    token = authorization[7:]
    auth_service = AuthService(session)
    user = await auth_service.get_current_user(token)

    from ai_team.domain.schemas.auth import UserResponse as UserResp

    return UserResp.from_user(user)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _project_error_response(exc: ProjectError) -> JSONResponse:
    """Map ProjectError to structured JSON response."""
    status_map: dict[str, int] = {
        "PROJECT_NOT_FOUND": 404,
        "INVALID_TIER": 422,
        "PROJECT_LIMIT_EXCEEDED": 403,
        "BUDGET_EXHAUSTED": 403,
        "PROJECT_ERROR": 500,
    }
    status_code = status_map.get(exc.code, 500)
    body = ErrorResponse(detail=exc.message, error_code=exc.code)
    return JSONResponse(status_code=status_code, content=body.model_dump())


# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------


@router.get(
    "/projects/tiers",
    response_model=list[TierInfo],
    summary="List available tiers",
)
async def list_tiers() -> list[TierInfo]:
    """
    Get all available subscription tiers with their features and pricing.
    """
    return [
        TierInfo(
            name=tier.name,
            display_name=tier.display_name,
            price_monthly=tier.price_monthly,
            tokens_per_project=tier.tokens_per_project,
            max_iterations=tier.max_iterations,
            max_projects=tier.max_projects,
            retention_days=tier.retention_days,
            can_download_code=tier.can_download_code,
        )
        for tier in TIERS.values()
    ]


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=201,
    summary="Create a new project",
)
async def create_project(
    request_body: CreateProjectRequest,
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse | JSONResponse:
    """
    Create a new project.

    - **name**: project name
    - **description**: natural language description of the app
    - **tier**: subscription tier (default: free)
    """
    try:
        # Validate tier
        if request_body.tier not in TIERS:
            from ai_team.domain.services.project_service import InvalidTierError

            raise InvalidTierError(request_body.tier)

        project = await project_service.create(
            user_id=current_user.id,
            name=request_body.name,
            description=request_body.description,
            tier=request_body.tier,
        )
        logger.info(
            "Project created: %s by user %s",
            project.name,
            current_user.email,
        )
        return ProjectResponse.from_project(project)
    except ProjectError as e:
        return _project_error_response(e)


@router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List user projects",
)
async def list_projects(
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    offset: int = 0,
    limit: int = 50,
    status: str | None = None,
) -> ProjectListResponse:
    """
    List all projects for the authenticated user.
    """
    projects, total = await project_service.list_by_user(
        current_user.id,
        offset=offset,
        limit=limit,
        status=status,
    )

    return ProjectListResponse(
        projects=[ProjectResponse.from_project(p) for p in projects],
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/projects/stats",
    response_model=ProjectStatsResponse,
    summary="Get user project stats",
)
async def get_project_stats(
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectStatsResponse:
    """
    Get project usage stats for the authenticated user.
    """
    stats = await project_service.get_user_stats(current_user.id)

    # Get tier info
    tier_config = get_tier("free")  # default tier
    total_projects = stats["total_projects"]
    max_projects = tier_config.max_projects
    projects_remaining = None if max_projects == -1 else max(0, max_projects - total_projects)

    return ProjectStatsResponse(
        total_projects=total_projects,
        projects_by_status=stats["projects_by_status"],
        total_tokens_used=stats["total_tokens_used"],
        current_tier="free",
        projects_remaining=projects_remaining,
    )


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get project details",
)
async def get_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse | JSONResponse:
    """
    Get details of a specific project.
    """
    try:
        project = await project_service.get(project_id, current_user.id)
        return ProjectResponse.from_project(project)
    except ProjectError as e:
        return _project_error_response(e)


@router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
)
async def update_project(
    project_id: str,
    request_body: UpdateProjectRequest,
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse | JSONResponse:
    """
    Update a project's name.
    """
    try:
        project = await project_service.update(
            project_id,
            current_user.id,
            name=request_body.name,
        )
        return ProjectResponse.from_project(project)
    except ProjectError as e:
        return _project_error_response(e)


@router.delete(
    "/projects/{project_id}",
    status_code=204,
    summary="Delete project",
    response_class=Response,
)
async def delete_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    """
    Delete a project.
    """
    try:
        await project_service.delete(project_id, current_user.id)
    except ProjectError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
