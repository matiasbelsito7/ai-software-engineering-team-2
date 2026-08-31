"""
FastAPI application dependencies.

Provides singletons for the Container and the compiled LangGraph.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any

from fastapi import Depends, Header

from ai_team.domain.schemas.auth import UserResponse
from ai_team.domain.services.auth_service import AuthService, InvalidTokenError
from ai_team.infrastructure.database.session import get_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from ai_team.infrastructure.container import Container


@lru_cache(maxsize=1)
def get_container() -> Container:
    """Return the singleton Container."""

    from ai_team.infrastructure.container import Container

    return Container()


@lru_cache(maxsize=1)
def get_graph() -> Any:
    """Build and compile the LangGraph workflow once."""

    from ai_team.graph.builder import GraphBuilder

    container = get_container()

    builder = GraphBuilder(
        spec=container.spec,
        planner=container.planner,
        architect=container.architect,
        backend=container.backend,
        frontend=container.frontend,
        reviewer=container.reviewer,
        qa=container.qa,
        documentation=container.documentation,
        devops=container.devops,
        git=container.git_agent,
    )

    return builder.build()


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """
    FastAPI dependency: extract and validate the current user from JWT.

    Use this dependency to protect endpoints that require authentication.
    """
    if not authorization.startswith("Bearer "):
        raise InvalidTokenError("Invalid authorization header format")

    token = authorization[7:]
    auth_service = AuthService(session)
    user = await auth_service.get_current_user(token)
    return UserResponse.from_user(user)


async def get_current_admin(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """
    FastAPI dependency: require admin role.

    Use this dependency to protect endpoints that require admin access.
    """
    if current_user.role != "admin":
        from ai_team.domain.services.auth_service import AuthError

        raise AuthError("Admin access required", "FORBIDDEN")
    return current_user
