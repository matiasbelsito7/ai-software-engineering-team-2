"""
HTTP client configuration.

Defines the shared HTTP timeouts used by every external
integration (LLM providers, Qdrant, GitHub, Docker, etc.).
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class HttpSettings(BaseSettings):
    """
    Shared HTTP client configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="HTTP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Timeouts (seconds)
    ###########################################################################

    connect_timeout: float = Field(
        default=10.0,
        gt=0,
        description="Timeout for establishing connections.",
    )

    read_timeout: float = Field(
        default=60.0,
        gt=0,
        description="Timeout for reading responses.",
    )

    write_timeout: float = Field(
        default=30.0,
        gt=0,
        description="Timeout for writing request payloads.",
    )

    pool_timeout: float = Field(
        default=10.0,
        gt=0,
        description="Timeout for acquiring a connection from the pool.",
    )
