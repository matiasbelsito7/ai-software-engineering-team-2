"""
Search tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class SearchTool(BaseTool):
    """
    Search the web or local documentation.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="search",
                description="Search the web or local documentation.",
                category="information",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        query = request.parameters.get("query", "")

        if not query:
            return ToolResult(
                success=False,
                error="Missing required parameter: query",
            )

        try:
            import subprocess
            import sys

            result = subprocess.run(
                [sys.executable, "-m", "websearch", query],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout.strip():
                return ToolResult(
                    success=True,
                    output=result.stdout.strip(),
                )

            return ToolResult(
                success=True,
                output=f"Search results for '{query}' not available via CLI.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
