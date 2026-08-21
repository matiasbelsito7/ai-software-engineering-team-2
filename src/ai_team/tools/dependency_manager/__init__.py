"""
Dependency manager tool.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class DependencyManagerTool(BaseTool):
    """
    Manage project dependencies via pip/uv.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="dependency_manager",
                description="Manage project dependencies (install, uninstall, list).",
                category="package_management",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        operation = request.parameters.get("operation", "install")
        package = request.parameters.get("package", "")

        import subprocess
        import sys

        try:
            if operation == "install":
                if not package:
                    return ToolResult(
                        success=False,
                        error="Missing required parameter: package",
                    )
                cmd = [sys.executable, "-m", "pip", "install", str(package)]

            elif operation == "uninstall":
                if not package:
                    return ToolResult(
                        success=False,
                        error="Missing required parameter: package",
                    )
                cmd = [sys.executable, "-m", "pip", "uninstall", "-y", str(package)]

            elif operation == "list":
                cmd = [sys.executable, "-m", "pip", "list"]

            elif operation == "freeze":
                cmd = [sys.executable, "-m", "pip", "freeze"]

            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported operation: {operation}",
                )

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "operation": operation,
                    "package": package,
                    "return_code": result.returncode,
                },
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )
