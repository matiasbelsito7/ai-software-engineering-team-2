"""
Filesystem tool.
"""

from __future__ import annotations

from ai_team.infrastructure.workspace import Workspace

from ai_team.tools.base import BaseTool
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)


class FilesystemTool(BaseTool):
    """
    Read and write files inside the workspace.
    """

    def __init__(
        self,
        *,
        workspace: Workspace,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="filesystem",
                description="Read and write files.",
                category="filesystem",
            ),
        )

        self._workspace = workspace

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get(
            "operation",
        )

        if operation == "read":
            return await self._read(request)

        if operation == "write":
            return await self._write(request)

        if operation == "exists":
            return await self._exists(request)

        return ToolResult(
            success=False,
            error=f"Unsupported operation: {operation}",
        )

    async def _read(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        path = self._workspace.resolve(
            request.parameters["path"],
        )

        content = path.read_text(
            encoding="utf-8",
        )

        return ToolResult(
            success=True,
            output=content,
        )

    async def _write(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        path = self._workspace.resolve(
            request.parameters["path"],
        )

        content = request.parameters["content"]

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return ToolResult(
            success=True,
            output=str(path.relative_to(self._workspace.root)),
        )

    async def _exists(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        exists = self._workspace.exists(
            request.parameters["path"],
        )

        return ToolResult(
            success=True,
            output=exists,
        )