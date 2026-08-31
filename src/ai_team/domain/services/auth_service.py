"""
Authentication service.

Handles user registration, login, JWT token management, and password hashing.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select

from ai_team.domain.models.user import User
from ai_team.infrastructure.config.security import SecuritySettings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security_settings = SecuritySettings()

# Password validation regex: min 8 chars, 1 uppercase, 1 lowercase, 1 number
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")


class AuthError(Exception):
    """Base authentication error."""

    def __init__(self, message: str, code: str = "AUTH_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class UserNotFoundError(AuthError):
    """User not found."""

    def __init__(self, identifier: str) -> None:
        super().__init__(f"User not found: {identifier}", "USER_NOT_FOUND")


class InvalidCredentialsError(AuthError):
    """Invalid email or password."""

    def __init__(self) -> None:
        super().__init__("Invalid email or password", "INVALID_CREDENTIALS")


class UserAlreadyExistsError(AuthError):
    """User with this email already exists."""

    def __init__(self, email: str) -> None:
        super().__init__(f"User already exists: {email}", "USER_ALREADY_EXISTS")


class InvalidTokenError(AuthError):
    """Invalid or expired token."""

    def __init__(self, detail: str = "Invalid or expired token") -> None:
        super().__init__(detail, "INVALID_TOKEN")


class InactiveUserError(AuthError):
    """User account is inactive."""

    def __init__(self) -> None:
        super().__init__("User account is inactive", "INACTIVE_USER")


class AuthService:
    """Authentication service for user management and JWT tokens."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -----------------------------------------------------------------
    # Password utilities
    # -----------------------------------------------------------------

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password with bcrypt."""
        return str(pwd_context.hash(password))

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bool(pwd_context.verify(plain_password, hashed_password))

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate password meets security requirements."""
        if not PASSWORD_PATTERN.match(password):
            raise AuthError(
                "Password must be at least 8 characters with "
                "1 uppercase, 1 lowercase, and 1 number.",
                "WEAK_PASSWORD",
            )

    # -----------------------------------------------------------------
    # JWT utilities
    # -----------------------------------------------------------------

    @staticmethod
    def create_access_token(user_id: str, role: str) -> str:
        """Create a JWT access token."""
        expire = datetime.now(timezone.utc) + timedelta(  # noqa: UP017
            minutes=security_settings.jwt_access_token_expire_minutes,
        )
        payload = {
            "sub": user_id,
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),  # noqa: UP017
        }
        return str(jwt.encode(
            payload,
            security_settings.jwt_secret,
            algorithm=security_settings.jwt_algorithm,
        ))

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        """Create a JWT refresh token."""
        expire = datetime.now(timezone.utc) + timedelta(  # noqa: UP017
            days=security_settings.jwt_refresh_token_expire_days,
        )
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),  # noqa: UP017
            "jti": str(uuid.uuid4()),
        }
        return str(jwt.encode(
            payload,
            security_settings.jwt_secret,
            algorithm=security_settings.jwt_algorithm,
        ))

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token,
                security_settings.jwt_secret,
                algorithms=[security_settings.jwt_algorithm],
            )
            return dict(payload)
        except JWTError as e:
            raise InvalidTokenError(str(e)) from e

    # -----------------------------------------------------------------
    # User operations
    # -----------------------------------------------------------------

    async def register(self, email: str, password: str) -> User:
        """Register a new user."""
        # Validate password
        self.validate_password(password)

        # Check if user exists
        existing = await self.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email)

        # Create user
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=self.hash_password(password),
            role="user",
            is_active=True,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(self, email: str, password: str) -> dict[str, Any]:
        """Authenticate user and return tokens."""
        user = await self.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError()

        if not self.verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        user_id = str(user.id)
        return {
            "access_token": self.create_access_token(user_id, user.role),
            "refresh_token": self.create_refresh_token(user_id),
            "token_type": "bearer",
            "expires_in": security_settings.jwt_access_token_expire_minutes * 60,
        }

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """Refresh an access token using a refresh token."""
        payload = self.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid token payload")

        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        if not user.is_active:
            raise InactiveUserError()

        return {
            "access_token": self.create_access_token(user_id, user.role),
            "refresh_token": self.create_refresh_token(user_id),
            "token_type": "bearer",
            "expires_in": security_settings.jwt_access_token_expire_minutes * 60,
        }

    async def get_current_user(self, token: str) -> User:
        """Get the current user from an access token."""
        payload = self.decode_token(token)

        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid token payload")

        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        if not user.is_active:
            raise InactiveUserError()

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        result = await self.session.execute(
            select(User).where(User.email == email),
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get a user by ID."""
        try:
            uid = uuid.UUID(user_id)
        except ValueError:
            return None
        result = await self.session.execute(
            select(User).where(User.id == uid),
        )
        return result.scalar_one_or_none()
