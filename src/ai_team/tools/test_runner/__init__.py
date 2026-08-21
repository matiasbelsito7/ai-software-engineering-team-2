"""
Test runner tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class TestRunnerTool(BaseTool):
    """
    Run tests using pytest.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="test_runner",
                description="Run tests using pytest.",
                category="testing",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        path = request.parameters.get("path", ".")
        markers = request.parameters.get("markers", "")
        verbose = request.parameters.get("verbose", True)

        import subprocess
        import sys

        cmd = [sys.executable, "-m", "pytest"]

        if path:
            cmd.append(str(path))

        if markers:
            cmd.extend(["-m", str(markers)])

        if verbose:
            cmd.append("-v")

        cmd.append("--tb=short")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "path": path,
                    "markers": markers,
                    "return_code": result.returncode,
                },
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error="pytest is not installed.",
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Tests timed out after 300 seconds.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
