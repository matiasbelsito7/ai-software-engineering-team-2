"""
Authentication API schemas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, EmailStr, Field

if TYPE_CHECKING:
    from datetime import datetime
    from typing import Any
    from uuid import UUID


# =====================================================================
# Request schemas
# =====================================================================


class RegisterRequest(BaseModel):
    """Request body for POST /auth/register."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(
        ...,
        description="User email address.",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (min 8 chars, 1 uppercase, 1 lowercase, 1 number).",
    )


class LoginRequest(BaseModel):
    """Request body for POST /auth/login."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(
        ...,
        description="User email address.",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User password.",
    )


class RefreshTokenRequest(BaseModel):
    """Request body for POST /auth/refresh."""

    model_config = ConfigDict(extra="forbid")

    refresh_token: str = Field(
        ...,
        description="JWT refresh token.",
    )


class UpdateProfileRequest(BaseModel):
    """Request body for PUT /auth/me."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr | None = Field(
        default=None,
        description="New email address.",
    )


class ForgotPasswordRequest(BaseModel):
    """Request body for POST /auth/forgot-password."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(
        ...,
        description="Email address to send reset link.",
    )


class ResetPasswordRequest(BaseModel):
    """Request body for POST /auth/reset-password."""

    model_config = ConfigDict(extra="forbid")

    token: str = Field(
        ...,
        description="Password reset token.",
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password (min 8 chars).",
    )


# =====================================================================
# Response schemas
# =====================================================================


class TokenResponse(BaseModel):
    """JWT token response."""

    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(
        ...,
        description="JWT access token.",
    )
    refresh_token: str = Field(
        ...,
        description="JWT refresh token.",
    )
    token_type: str = Field(
        default="bearer",
        description="Token type.",
    )
    expires_in: int = Field(
        ...,
        description="Access token expiration in seconds.",
    )


class UserResponse(BaseModel):
    """User profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    role: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_user(cls, user: Any) -> UserResponse:
        """Create response from User ORM model."""
        return cls(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )


class MessageResponse(BaseModel):
    """Generic message response."""

    model_config = ConfigDict(extra="forbid")

    message: str
