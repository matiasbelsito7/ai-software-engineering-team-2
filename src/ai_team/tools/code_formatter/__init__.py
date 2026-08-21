"""
Code formatter tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class CodeFormatterTool(BaseTool):
    """
    Format code using black/ruff.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="code_formatter",
                description="Format code using black or ruff.",
                category="code_quality",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        path = request.parameters.get("path", ".")
        formatter = request.parameters.get("formatter", "ruff")

        if not path:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        import subprocess
        import sys

        try:
            if formatter == "black":
                cmd = [sys.executable, "-m", "black", str(path)]
            else:
                cmd = [sys.executable, "-m", "ruff", "format", str(path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "formatter": formatter,
                    "return_code": result.returncode,
                },
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"{formatter} is not installed.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
