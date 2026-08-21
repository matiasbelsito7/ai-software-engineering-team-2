"""
Repository tool.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class RepositoryTool(BaseTool):
    """
    Browse and inspect a software repository.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="repository",
                description="Browse and inspect a software repository.",
                category="filesystem",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        operation = request.parameters.get("operation", "list")
        path_str = request.parameters.get("path", ".")

        try:
            if operation == "list":
                return self._list(path_str)
            elif operation == "tree":
                return self._tree(path_str)
            elif operation == "read":
                return self._read(request.parameters)
            elif operation == "info":
                return self._info(path_str)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported operation: {operation}",
                )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

    def _list(self, path_str: str) -> ToolResult:
        root = Path(path_str)

        if not root.exists():
            return ToolResult(
                success=False,
                error=f"Path not found: {path_str}",
            )

        entries: list[str] = []

        for entry in sorted(root.iterdir()):
            prefix = "d" if entry.is_dir() else "f"
            entries.append(f"[{prefix}] {entry.name}")

        return ToolResult(
            success=True,
            output=entries,
            metadata={"path": str(root), "count": len(entries)},
        )

    def _tree(self, path_str: str) -> ToolResult:
        root = Path(path_str)

        if not root.exists():
            return ToolResult(
                success=False,
                error=f"Path not found: {path_str}",
            )

        skip = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".mypy_cache",
            ".ruff_cache",
            "dist",
            "build",
        }

        lines: list[str] = []
        self._walk_tree(root, root, lines, skip, depth=0)

        return ToolResult(
            success=True,
            output="\n".join(lines),
            metadata={"count": len(lines)},
        )

    def _walk_tree(
        self,
        root: Path,
        current: Path,
        lines: list[str],
        skip: set[str],
        depth: int,
    ) -> None:
        if depth > 6 or len(lines) > 500:
            return

        try:
            entries = sorted(current.iterdir())
        except PermissionError:
            return

        for entry in entries:
            if entry.name in skip:
                continue

            indent = "  " * depth
            prefix = "d" if entry.is_dir() else "f"
            lines.append(f"{indent}[{prefix}] {entry.name}")

            if entry.is_dir():
                self._walk_tree(root, entry, lines, skip, depth + 1)

    def _read(self, params: dict[str, object]) -> ToolResult:
        path_str = str(params.get("path", ""))

        if not path_str:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        path = Path(path_str)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"File not found: {path_str}",
            )

        content = path.read_text(encoding="utf-8", errors="ignore")

        return ToolResult(
            success=True,
            output=content,
            metadata={"path": str(path), "size": len(content)},
        )

    def _info(self, path_str: str) -> ToolResult:
        root = Path(path_str)

        if not root.exists():
            return ToolResult(
                success=False,
                error=f"Path not found: {path_str}",
            )

        files = list(root.rglob("*"))
        py_files = [f for f in files if f.suffix == ".py"]
        total_size = sum(f.stat().st_size for f in files if f.is_file())

        return ToolResult(
            success=True,
            output={
                "total_files": len(files),
                "python_files": len(py_files),
                "total_size_bytes": total_size,
                "root": str(root),
            },
        )
