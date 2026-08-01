```python
"""
Application configuration.

Defines the core settings required to run the AI Software Engineering Team
application.

This module is intentionally limited to application-level configuration.
Infrastructure-specific settings (database, Redis, Qdrant, LLM, telemetry,
etc.) live in their own modules.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_team.shared.enums import Environment


class AppSettings(BaseSettings):
    """
    Core application settings.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Application
    ###########################################################################

    name: str = Field(
        default="AI Software Engineering Team",
        description="Application name.",
    )

    version: str = Field(
        default="0.1.0",
        description="Current application version.",
    )

    description: str = Field(
        default="Production-ready multi-agent AI software engineering platform.",
        description="Application description.",
    )

    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Current runtime environment.",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode.",
    )

    ###########################################################################
    # HTTP Server
    ###########################################################################

    host: str = Field(
        default="0.0.0.0",
        description="Application host.",
    )

    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Application port.",
    )

    reload: bool = Field(
        default=False,
        description="Enable auto reload (development only).",
    )

    workers: int = Field(
        default=1,
        ge=1,
        description="Number of application workers.",
    )

    ###########################################################################
    # API
    ###########################################################################

    api_prefix: str = Field(
        default="/api/v1",
        description="REST API prefix.",
    )

    docs_url: str = Field(
        default="/docs",
        description="Swagger UI endpoint.",
    )

    redoc_url: str = Field(
        default="/redoc",
        description="ReDoc endpoint.",
    )

    openapi_url: str = Field(
        default="/openapi.json",
        description="OpenAPI schema endpoint.",
    )

    ###########################################################################
    # CORS
    ###########################################################################

    allowed_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS origins.",
    )

    allowed_methods: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed HTTP methods.",
    )

    allowed_headers: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed HTTP headers.",
    )

    allow_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS.",
    )
```
