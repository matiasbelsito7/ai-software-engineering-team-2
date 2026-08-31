"""
Authentication router.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

from ai_team.app.api.schemas.tasks import ErrorResponse
from ai_team.domain.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from ai_team.domain.services.auth_service import (
    AuthError,
    AuthService,
    InvalidTokenError,
    UserNotFoundError,
)
from ai_team.infrastructure.database.session import get_session

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


# ---------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[AuthService, None]:
    """Yield an AuthService instance."""
    yield AuthService(session)


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """FastAPI dependency: extract and validate the current user from JWT."""
    if not authorization.startswith("Bearer "):
        raise InvalidTokenError("Invalid authorization header format")

    token = authorization[7:]
    user = await auth_service.get_current_user(token)
    return UserResponse.from_user(user)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _auth_error_response(exc: AuthError) -> JSONResponse:
    """Map AuthError to structured JSON response."""
    status_map: dict[str, int] = {
        "USER_NOT_FOUND": 404,
        "INVALID_CREDENTIALS": 401,
        "USER_ALREADY_EXISTS": 409,
        "INVALID_TOKEN": 401,
        "INACTIVE_USER": 403,
        "WEAK_PASSWORD": 422,
        "AUTH_ERROR": 500,
    }
    status_code = status_map.get(exc.code, 500)
    body = ErrorResponse(detail=exc.message, error_code=exc.code)
    return JSONResponse(status_code=status_code, content=body.model_dump())


# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
async def register(
    request_body: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse | JSONResponse:
    """
    Create a new user account.

    - **email**: valid email address
    - **password**: min 8 chars, 1 uppercase, 1 lowercase, 1 number
    """
    try:
        user = await auth_service.register(
            email=request_body.email,
            password=request_body.password,
        )
        logger.info("New user registered: %s", user.email)
        return UserResponse.from_user(user)
    except AuthError as e:
        return _auth_error_response(e)


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Login and get JWT tokens",
)
async def login(
    request_body: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse | JSONResponse:
    """
    Authenticate with email and password.

    Returns access and refresh JWT tokens.
    """
    try:
        tokens = await auth_service.login(
            email=request_body.email,
            password=request_body.password,
        )
        logger.info("User logged in: %s", request_body.email)
        return TokenResponse(**tokens)
    except AuthError as e:
        return _auth_error_response(e)


@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
async def refresh_token(
    request_body: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse | JSONResponse:
    """
    Get a new access token using a refresh token.
    """
    try:
        tokens = await auth_service.refresh_token(
            refresh_token=request_body.refresh_token,
        )
        return TokenResponse(**tokens)
    except AuthError as e:
        return _auth_error_response(e)


@router.get(
    "/auth/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """
    Get the authenticated user's profile.

    Requires a valid Bearer token in the Authorization header.
    """
    return current_user


@router.put(
    "/auth/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_me(
    request_body: UpdateProfileRequest,
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse | JSONResponse:
    """
    Update the authenticated user's profile.

    Currently only supports email update.
    """
    try:
        if request_body.email:
            user = await auth_service.get_user_by_id(str(current_user.id))
            if user is None:
                raise UserNotFoundError(str(current_user.id))
            user.email = request_body.email
            await auth_service.session.commit()
            await auth_service.session.refresh(user)
            return UserResponse.from_user(user)
        return current_user
    except AuthError as e:
        return _auth_error_response(e)


@router.post(
    "/auth/forgot-password",
    response_model=dict[str, str],
    summary="Request password reset",
)
async def forgot_password(
    request_body: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    """
    Request a password reset link.

    In production, this would send an email. For now, returns a generic message.
    """
    user = await auth_service.get_user_by_email(request_body.email)
    if user:
        logger.info("Password reset requested for: %s", request_body.email)
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a reset link has been sent."}


@router.post(
    "/auth/reset-password",
    response_model=dict[str, str],
    summary="Reset password with token",
)
async def reset_password(
    request_body: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str] | JSONResponse:
    """
    Reset password using a valid reset token.
    """
    try:
        payload = auth_service.decode_token(request_body.token)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid reset token")

        user = await auth_service.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        auth_service.validate_password(request_body.new_password)
        user.password_hash = auth_service.hash_password(request_body.new_password)
        await auth_service.session.commit()

        return {"message": "Password has been reset successfully."}
    except AuthError as e:
        return _auth_error_response(e)
