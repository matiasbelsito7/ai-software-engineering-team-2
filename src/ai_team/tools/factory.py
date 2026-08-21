"""
Tool factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.tools.filesystem import FilesystemTool
from ai_team.tools.git import GitTool
from ai_team.tools.manager import ToolManager
from ai_team.tools.terminal import TerminalTool

if TYPE_CHECKING:
    from ai_team.infrastructure.workspace import Workspace


def build_tools(
    *,
    workspace: Workspace,
) -> ToolManager:
    """
    Build the application tool registry.
    """

    terminal = TerminalTool(
        workspace=workspace,
    )

    tools = [
        FilesystemTool(
            workspace=workspace,
        ),
        terminal,
        GitTool(
            terminal=terminal,
        ),
    ]

    tool_manager = ToolManager()

    for tool in tools:
        tool_manager.register(tool)

    return tool_manager
