"""
Git tool.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.tools.base import BaseTool
from ai_team.tools.git import commands
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from ai_team.tools.terminal import TerminalTool


class GitTool(BaseTool):
    """
    High-level Git operations.
    """

    def __init__(
        self,
        *,
        terminal: TerminalTool,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="git",
                description="Execute Git operations.",
                category="version_control",
            ),
        )

        self._terminal = terminal

        self._operations: dict[
            str,
            Callable[[dict[str, Any]], str],
        ] = {
            # Core operations
            "status": lambda _: commands.status(),
            "diff": lambda _: commands.diff(),
            "diff_staged": lambda _: commands.diff_staged(),
            "diff_name_only": lambda _: commands.diff_name_only(),
            "branch": lambda _: commands.branch(),
            "checkout": lambda p: commands.checkout(p["branch"]),
            "add": lambda p: commands.add(p.get("path", ".")),
            "commit": lambda p: commands.commit(p["message"]),
            "log": lambda p: commands.log(p.get("limit", 10)),
            "log_detailed": lambda p: commands.log_detailed(p.get("limit", 5)),
            "restore": lambda p: commands.restore(p["path"]),
            "init": lambda _: commands.init(),
            "clone": lambda p: commands.clone(p["repository"]),
            "pull": lambda _: commands.pull(),
            "push": lambda _: commands.push(),
            "push_upstream": lambda p: commands.push_upstream(p["branch"]),
            # Branch management
            "create_branch": lambda p: commands.create_branch(p["branch"]),
            "create_and_checkout": lambda p: commands.create_and_checkout(p["branch"]),
            "delete_branch": lambda p: commands.delete_branch(p["branch"], p.get("force", False)),
            "rename_branch": lambda p: commands.rename_branch(p["old"], p["new"]),
            "merge": lambda p: commands.merge_branch(p["branch"]),
            "fetch": lambda _: commands.fetch(),
            "list_branches_remote": lambda _: commands.list_branches_remote(),
            # Tag operations
            "create_tag": lambda p: commands.create_tag(p["tag"], p.get("message")),
            "list_tags": lambda _: commands.list_tags(),
            "delete_tag": lambda p: commands.delete_tag(p["tag"]),
            # Stash operations
            "stash": lambda p: commands.stash(p.get("message")),
            "stash_pop": lambda _: commands.stash_pop(),
            "stash_list": lambda _: commands.stash_list(),
            "stash_drop": lambda _: commands.stash_drop(),
            # Remote operations
            "add_remote": lambda p: commands.add_remote(p["name"], p["url"]),
            "list_remotes": lambda _: commands.list_remotes(),
            "remove_remote": lambda p: commands.remove_remote(p["name"]),
            # PR operations (requires gh CLI)
            "create_pr": lambda p: commands.create_pr(
                p["title"], p["body"], p.get("base", "main"), p.get("head")
            ),
            "list_prs": lambda p: commands.list_prs(p.get("state", "open")),
            "view_pr": lambda p: commands.view_pr(p.get("number")),
            "checkout_pr": lambda p: commands.checkout_pr(p["number"]),
            "merge_pr": lambda p: commands.merge_pr(p["number"]),
            "close_pr": lambda p: commands.close_pr(p["number"]),
            # Repository info
            "repo_url": lambda _: commands.repo_url(),
            "current_branch": lambda _: commands.current_branch(),
            "commit_count": lambda _: commands.commit_count(),
            "last_commit": lambda _: commands.last_commit(),
        }

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get("operation")

        assert operation is not None

        builder = self._operations.get(operation)

        if builder is None:
            return ToolResult(
                success=False,
                error=f"Unknown Git operation '{operation}'.",
            )

        command = builder(request.parameters)

        return await self._terminal.run(
            ToolRequest(
                parameters={"command": command},
            )
        )
