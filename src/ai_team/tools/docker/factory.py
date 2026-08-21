"""
Docker tool factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.tools.docker.docker import DockerTool
from ai_team.tools.docker.policy import DockerPolicy

if TYPE_CHECKING:
    from ai_team.tools.docker.manager import DockerManager


def build_docker_tool(
    *,
    manager: DockerManager,
) -> DockerTool:
    """
    Build the Docker tool.
    """

    policy = DockerPolicy()

    return DockerTool(
        manager=manager,
        policy=policy,
    )
