"""
Git tool.
"""

from __future__ import annotations

from collections.abc import Callable

from ai_team.tools.base import BaseTool
from ai_team.tools.git import commands
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)
from ai_team.tools.terminal import TerminalTool


class GitTool(BaseTool):
    """
    High-level Git operations.
    """

    def __init__(
        self,
        *,
        terminal: TerminalTool,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="git",
                description="Execute Git operations.",
                category="version_control",
            ),
        )

        self._terminal = terminal

        self._operations: dict[
            str,
            Callable[[dict], str],
        ] = {

            "status": lambda _: commands.status(),

            "diff": lambda _: commands.diff(),

            "branch": lambda _: commands.branch(),

            "checkout": (
                lambda p:
                commands.checkout(
                    p["branch"],
                )
            ),

            "add": (
                lambda p:
                commands.add(
                    p.get(
                        "path",
                        ".",
                    ),
                )
            ),

            "commit": (
                lambda p:
                commands.commit(
                    p["message"],
                )
            ),

            "log": (
                lambda p:
                commands.log(
                    p.get(
                        "limit",
                        10,
                    ),
                )
            ),

            "restore": (
                lambda p:
                commands.restore(
                    p["path"],
                )
            ),

            "init": lambda _: commands.init(),

            "clone": (
                lambda p:
                commands.clone(
                    p["repository"],
                )
            ),

            "pull": lambda _: commands.pull(),

            "push": lambda _: commands.push(),
        }

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get(
            "operation",
        )

        builder = self._operations.get(
            operation,
        )

        if builder is None:

            return ToolResult(
                success=False,
                error=(
                    f"Unknown Git operation "
                    f"'{operation}'."
                ),
            )

        command = builder(
            request.parameters,
        )

        return await self._terminal.run(
            ToolRequest(
                parameters={
                    "command": command,
                },
            )
        )