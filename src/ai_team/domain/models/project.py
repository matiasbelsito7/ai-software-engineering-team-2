"""
Project ORM model.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ai_team.infrastructure.database.base import Base


class Project(Base):
    """Project model representing a generated application."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    tier: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="free",
    )
    tokens_used: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    iterations_used: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )
    files_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Project {self.name} ({self.status})>"

    @classmethod
    def create(
        cls,
        *,
        user_id: uuid.UUID,
        name: str,
        description: str,
        tier: str,
        retention_days: int,
    ) -> Project:
        """Create a new project with proper expiration."""
        now = datetime.now(timezone.utc)  # noqa: UP017
        return cls(
            user_id=user_id,
            name=name,
            description=description,
            tier=tier,
            expires_at=now + timedelta(days=retention_days),
        )
