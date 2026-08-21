"""
Type checker tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class TypeCheckerTool(BaseTool):
    """
    Run type checking with mypy or pyright.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="type_checker",
                description="Run static type checking on code.",
                category="code_quality",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        path = request.parameters.get("path", "src/")
        checker = request.parameters.get("checker", "mypy")

        import subprocess
        import sys

        try:
            if checker == "pyright":
                cmd = [sys.executable, "-m", "pyright", str(path)]
            else:
                cmd = [sys.executable, "-m", "mypy", str(path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout or "No type errors found.",
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "checker": checker,
                    "return_code": result.returncode,
                },
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"{checker} is not installed.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
