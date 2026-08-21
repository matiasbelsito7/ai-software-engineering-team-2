"""
Terminal tool.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from ai_team.tools.base import BaseTool
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)
from ai_team.tools.terminal.policy import (
    CommandPolicy,
)

if TYPE_CHECKING:
    from ai_team.infrastructure.workspace import Workspace


class TerminalTool(BaseTool):
    """
    Execute terminal commands inside the workspace.
    """

    def __init__(
        self,
        *,
        workspace: Workspace,
        policy: CommandPolicy | None = None,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="terminal",
                description="Execute shell commands.",
                category="execution",
            ),
        )

        self._workspace = workspace

        self._policy = policy or CommandPolicy()

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
            self._policy.validate(
                command,
                cwd=self._workspace.cwd,
            )

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
