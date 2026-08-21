"""
Python execution policy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from ai_team.infrastructure.workspace import Workspace


class PythonPolicy:
    """
    Validates Python operations before execution.
    """

    ALLOWED_EXTENSIONS: ClassVar[set[str]] = {
        ".py",
    }

    def validate_script(
        self,
        workspace: Workspace,
        script: str,
    ) -> None:
        """
        Validate a Python script.
        """

        path = workspace.resolve(script)

        if path.suffix not in self.ALLOWED_EXTENSIONS:
            raise PermissionError(f"Unsupported file type: {path.suffix}")

    def validate_module(
        self,
        module: str,
    ) -> None:
        """
        Validate module execution.
        """

        if not module.strip():
            raise PermissionError("Module name cannot be empty.")

    def validate_package(
        self,
        package: str,
    ) -> None:
        """
        Validate pip package.
        """

        if not package.strip():
            raise PermissionError("Package name cannot be empty.")

    def validate_inline_code(
        self,
        code: str,
    ) -> None:
        """
        Validate inline Python code.
        """

        if not code.strip():
            raise PermissionError("Python code cannot be empty.")
