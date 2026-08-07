"""
HTTP tool factory.
"""

from __future__ import annotations

from ai_team.tools.http.http import HttpTool
from ai_team.tools.http.manager import HttpManager
from ai_team.tools.http.policy import HttpPolicy


def build_http_tool(
    *,
    manager: HttpManager,
) -> HttpTool:
    """
    Build the HTTP tool.
    """

    policy = HttpPolicy()

    return HttpTool(
        manager=manager,
        policy=policy,
    )