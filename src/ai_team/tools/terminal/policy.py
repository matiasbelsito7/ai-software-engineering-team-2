"""
Terminal command execution policy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from pathlib import Path


class CommandPolicy:
    """
    Validates whether a command can be executed.
    """

    DEFAULT_BLOCKED_COMMANDS: ClassVar[set[str]] = {
        "rm",
        "rmdir",
        "del",
        "format",
        "mkfs",
        "shutdown",
        "reboot",
        "poweroff",
        "sudo",
        "su",
        "passwd",
        "chmod",
        "chown",
    }

    REQUIRES_APPROVAL_COMMANDS: ClassVar[set[str]] = {
        "git push",
        "git push --force",
        "git push -f",
        "git clone",
        "git commit",
        "git reset --hard",
        "git clean",
        "gh pr merge",
        "gh pr create",
        "docker run",
        "docker compose up",
    }

    def __init__(
        self,
        *,
        blocked_commands: set[str] | None = None,
        approval_commands: set[str] | None = None,
    ) -> None:

        self._blocked_commands = blocked_commands or self.DEFAULT_BLOCKED_COMMANDS
        self._approval_commands = approval_commands or self.REQUIRES_APPROVAL_COMMANDS

    def validate(
        self,
        command: str,
        *,
        cwd: Path,
    ) -> None:
        """
        Raises PermissionError if the command is not allowed.
        """

        stripped = command.strip()

        if not stripped:
            raise PermissionError("Empty command.")

        executable = stripped.split()[0].lower()

        if executable in self._blocked_commands:
            raise PermissionError(f"Command '{executable}' is blocked.")

    def requires_approval(self, command: str) -> bool:
        """
        Returns True if the command requires human approval before execution.
        """

        stripped = command.strip().lower()

        if not stripped:
            return False

        for blocked in self._approval_commands:
            if stripped == blocked or stripped.startswith(blocked + " "):
                return True

        return False
