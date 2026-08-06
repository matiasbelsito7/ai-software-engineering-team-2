"""
Terminal tool.
"""

from __future__ import annotations

import asyncio

from ai_team.infrastructure.workspace import Workspace

from ai_team.tools.base import BaseTool
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)


class TerminalTool(BaseTool):
    """
    Execute shell commands inside the workspace.
    """

    def __init__(
        self,
        *,
        workspace: Workspace,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="terminal",
                description="Execute terminal commands.",
                category="execution",
            ),
        )

        self._workspace = workspace

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        command = request.parameters.get(
            "command",
        )

        timeout = request.parameters.get(
            "timeout",
            60,
        )

        if command is None:
            return ToolResult(
                success=False,
                error="Missing command.",
            )

        try:

            process = await asyncio.create_subprocess_shell(
                command,
                cwd=self._workspace.cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )

            return ToolResult(
                success=process.returncode == 0,
                output=stdout.decode(
                    "utf-8",
                ),
                error=stderr.decode(
                    "utf-8",
                )
                or None,
                metadata={
                    "return_code": process.returncode,
                },
            )

        except TimeoutError:

            process.kill()

            await process.wait()

            return ToolResult(
                success=False,
                error="Command timeout.",
            )

        except Exception as exc:

            return ToolResult(
                success=False,
                error=str(exc),
            )