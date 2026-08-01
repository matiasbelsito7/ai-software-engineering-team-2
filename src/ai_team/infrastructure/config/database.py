```python
"""
Database configuration.

Defines all PostgreSQL and SQLAlchemy settings.

This module only contains configuration.
Engine and Session creation belong to:

    infrastructure/database/
"""

from __future__ import annotations

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    PostgreSQL configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Connection
    ###########################################################################

    host: str = Field(
        default="localhost",
        description="Database host.",
    )

    port: int = Field(
        default=5432,
        ge=1,
        le=65535,
        description="Database port.",
    )

    database: str = Field(
        default="ai_team",
        description="Database name.",
    )

    username: str = Field(
        default="postgres",
        description="Database username.",
    )

    password: str = Field(
        default="postgres",
        description="Database password.",
    )

    ###########################################################################
    # SQLAlchemy
    ###########################################################################

    echo: bool = Field(
        default=False,
        description="Enable SQLAlchemy SQL logging.",
    )

    pool_size: int = Field(
        default=10,
        ge=1,
        description="Connection pool size.",
    )

    max_overflow: int = Field(
        default=20,
        ge=0,
        description="Maximum overflow connections.",
    )

    pool_timeout: int = Field(
        default=30,
        ge=1,
        description="Pool timeout (seconds).",
    )

    pool_recycle: int = Field(
        default=1800,
        ge=0,
        description="Recycle idle connections (seconds).",
    )

    ###########################################################################
    # Connection Health
    ###########################################################################

    pool_pre_ping: bool = Field(
        default=True,
        description="Validate connections before use.",
    )

    ###########################################################################
    # Driver
    ###########################################################################

    driver: str = Field(
        default="asyncpg",
        description="SQLAlchemy async driver.",
    )

    ###########################################################################
    # Alembic
    ###########################################################################

    alembic_table: str = Field(
        default="alembic_version",
        description="Alembic version table.",
    )

    ###########################################################################
    # URL
    ###########################################################################

    @computed_field
    @property
    def url(self) -> str:
        """
        SQLAlchemy async connection URL.
        """

        return (
            f"postgresql+{self.driver}://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
```
