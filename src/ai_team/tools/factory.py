"""
Tool factory.
"""

from __future__ import annotations

from ai_team.infrastructure.workspace import Workspace

from ai_team.tools.manager import ToolManager

from ai_team.tools.filesystem import FilesystemTool
from ai_team.tools.git import GitTool
from ai_team.tools.terminal import TerminalTool


def build_tools(
    *,
    workspace: Workspace,
) -> ToolManager:
    """
    Build the application tool registry.
    """

    tools = [

        FilesystemTool(
            workspace=workspace,
        ),

        TerminalTool(
            workspace=workspace,
        ),

        GitTool(
            workspace=workspace,
        ),

    ]

    return ToolManager(
        tools=tools,
    )