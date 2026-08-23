"""
Terminal tool.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING
from uuid import uuid4

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
    from ai_team.app.api.task_store import TaskStore
    from ai_team.infrastructure.workspace import Workspace

logger = logging.getLogger(__name__)


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

        self._task_store: TaskStore | None = None

        self._task_id: str | None = None

        self._agent: str | None = None

    def set_approval_context(
        self,
        *,
        task_store: TaskStore | None = None,
        task_id: str | None = None,
        agent: str | None = None,
    ) -> None:
        """Set the context for human-in-the-loop approval."""

        self._task_store = task_store

        self._task_id = task_id

        self._agent = agent

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

            if (
                self._policy.requires_approval(command)
                and self._task_store is not None
                and self._task_id is not None
            ):
                approved = await self._request_approval(command)

                if not approved:
                    return ToolResult(
                        success=False,
                        error=f"Command rejected by user: {command}",
                        metadata={"rejected": True},
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

    async def _request_approval(self, command: str) -> bool:
        """Request human approval for a command."""

        approval_id = str(uuid4())

        assert self._task_store is not None
        assert self._task_id is not None

        await self._task_store.request_approval(
            self._task_id,
            approval_id=approval_id,
            command=command,
            agent=self._agent,
            description=f"The agent wants to execute: {command}",
        )

        logger.info(
            "Approval requested for command '%s' in task %s",
            command,
            self._task_id,
        )

        approved = await self._task_store.wait_approval(
            approval_id,
            timeout=300.0,
        )

        if not approved:
            logger.warning(
                "Approval timed out or failed for command '%s' in task %s",
                command,
                self._task_id,
            )

        return approved
