"""
Docker tool factory.
"""

from __future__ import annotations

from ai_team.tools.docker.docker import DockerTool
from ai_team.tools.docker.manager import DockerManager
from ai_team.tools.docker.policy import DockerPolicy


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