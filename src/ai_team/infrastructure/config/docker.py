"""
Docker configuration.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DockerSettings(BaseSettings):
    """
    Docker daemon and container management settings.
    """

    model_config = SettingsConfigDict(
        env_prefix="DOCKER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Daemon
    ###########################################################################

    host: str = Field(
        default="unix:///var/run/docker.sock",
        description="Docker daemon socket or TCP address.",
    )

    tls: bool = Field(
        default=False,
        description="Enable TLS for Docker daemon connection.",
    )

    timeout: int = Field(
        default=60,
        ge=1,
        description="Default timeout in seconds for Docker API calls.",
    )

    ###########################################################################
    # Containers
    ###########################################################################

    default_network: str = Field(
        default="bridge",
        description="Default Docker network for containers.",
    )

    auto_remove: bool = Field(
        default=False,
        description="Automatically remove containers when they stop.",
    )

    privileged: bool = Field(
        default=False,
        description="Allow running privileged containers.",
    )

    ###########################################################################
    # Security
    ###########################################################################

    blocked_images: list[str] = Field(
        default_factory=lambda: [
            "docker:dind",
            "docker:latest",
        ],
        description="Images that cannot be pulled or run.",
    )

    max_containers: int = Field(
        default=50,
        ge=1,
        description="Maximum number of concurrent containers.",
    )

    ###########################################################################
    # Workspace
    ###########################################################################

    workspace_mount: str = Field(
        default="./workspace:/app/workspace",
        description="Host:container volume mount for workspace.",
    )
