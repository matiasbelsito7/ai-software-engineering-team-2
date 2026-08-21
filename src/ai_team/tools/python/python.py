"""
Python tool.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.tools.base import BaseTool
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)
from ai_team.tools.python import commands

if TYPE_CHECKING:
    from collections.abc import Callable

    from ai_team.tools.terminal import TerminalTool


class PythonTool(BaseTool):
    """
    High-level Python operations.
    """

    def __init__(
        self,
        *,
        terminal: TerminalTool,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="python",
                description="Execute Python operations.",
                category="execution",
            ),
        )

        self._terminal = terminal

        self._operations: dict[
            str,
            Callable[[dict[str, Any]], str],
        ] = {

            "run_script": (
                lambda p:
                commands.run_script(
                    p["script"],
                )
            ),

            "run_module": (
                lambda p:
                commands.run_module(
                    p["module"],
                )
            ),

            "run_code": (
                lambda p:
                commands.run_code(
                    p["code"],
                )
            ),

            "pip_install": (
                lambda p:
                commands.pip_install(
                    p["package"],
                )
            ),

            "pip_uninstall": (
                lambda p:
                commands.pip_uninstall(
                    p["package"],
                )
            ),

            "format": (
                lambda p:
                commands.format_script(
                    p["script"],
                )
            ),

            "lint": (
                lambda p:
                commands.lint_script(
                    p["script"],
                )
            ),

            "test": (
                lambda p:
                commands.test(
                    p.get(
                        "path",
                        ".",
                    ),
                )
            ),
        }

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get(
            "operation",
        )

        assert operation is not None

        builder = self._operations.get(
            operation,
        )

        if builder is None:

            return ToolResult(
                success=False,
                error=(
                    f"Unknown Python operation "
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
