"""
Redis configuration.

Defines the Redis configuration used throughout the application.

Redis is responsible for:

- Cache
- LangGraph checkpoints
- Distributed locks
- Event bus
- Task queues (future)
"""

from __future__ import annotations

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """
    Redis configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
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
        description="Redis host.",
    )

    port: int = Field(
        default=6379,
        ge=1,
        le=65535,
        description="Redis port.",
    )

    database: int = Field(
        default=0,
        ge=0,
        description="Redis database number.",
    )

    password: str | None = Field(
        default=None,
        description="Redis password.",
    )

    username: str | None = Field(
        default=None,
        description="Redis username (Redis ACL).",
    )

    ###########################################################################
    # Connection Pool
    ###########################################################################

    max_connections: int = Field(
        default=50,
        gt=0,
        description="Maximum number of Redis connections.",
    )

    socket_timeout: float = Field(
        default=5.0,
        gt=0,
        description="Socket timeout in seconds.",
    )

    socket_connect_timeout: float = Field(
        default=5.0,
        gt=0,
        description="Connection timeout in seconds.",
    )

    health_check_interval: int = Field(
        default=30,
        ge=0,
        description="Connection health check interval.",
    )

    ###########################################################################
    # Cache
    ###########################################################################

    default_ttl: int = Field(
        default=3600,
        gt=0,
        description="Default cache TTL (seconds).",
    )

    key_prefix: str = Field(
        default="ai-team",
        description="Redis key prefix.",
    )

    ###########################################################################
    # LangGraph
    ###########################################################################

    checkpoint_prefix: str = Field(
        default="langgraph",
        description="Checkpoint key prefix.",
    )

    ###########################################################################
    # Task Queue
    ###########################################################################

    queue_name: str = Field(
        default="default",
        description="Default queue name.",
    )

    ###########################################################################
    # URL
    ###########################################################################

    @property
    @computed_field
    def url(self) -> str:
        """
        Redis connection URL.
        """

        auth = ""

        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"

        elif self.password:
            auth = f":{self.password}@"

        return (
            f"redis://{auth}"
            f"{self.host}:{self.port}/"
            f"{self.database}"
        )
