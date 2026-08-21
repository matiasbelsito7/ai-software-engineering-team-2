"""
Linter tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class LinterTool(BaseTool):
    """
    Lint code using ruff or flake8.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="linter",
                description="Lint code for style and error detection.",
                category="code_quality",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        path = request.parameters.get("path", ".")
        linter = request.parameters.get("linter", "ruff")

        if not path:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        import subprocess
        import sys

        try:
            if linter == "flake8":
                cmd = [sys.executable, "-m", "flake8", str(path)]
            else:
                cmd = [sys.executable, "-m", "ruff", "check", str(path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout or "No issues found.",
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "linter": linter,
                    "return_code": result.returncode,
                },
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"{linter} is not installed.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
