"""
Code analyzer tool.
"""

from __future__ import annotations

import ast
from pathlib import Path

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class CodeAnalyzerTool(BaseTool):
    """
    Analyze code structure and quality.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="code_analyzer",
                description="Analyze code structure, imports, and quality metrics.",
                category="code_quality",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        path = request.parameters.get("path", ".")

        if not path:
            return ToolResult(
                success=False,
                error="Missing required parameter: path",
            )

        try:
            target = Path(path)

            if target.is_file():
                return self._analyze_file(target)
            elif target.is_dir():
                return self._analyze_dir(target)
            else:
                return ToolResult(
                    success=False,
                    error=f"Path not found: {path}",
                )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

    def _analyze_file(self, path: Path) -> ToolResult:
        content = path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()

        try:
            tree = ast.parse(content, filename=str(path))
        except SyntaxError as exc:
            return ToolResult(
                success=False,
                error=f"Syntax error in {path}: {exc}",
            )

        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        imports = [
            ast.dump(node)
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "lines": len(lines),
                "classes": classes,
                "functions": functions,
                "import_count": len(imports),
            },
        )

    def _analyze_dir(self, path: Path) -> ToolResult:
        py_files = list(path.rglob("*.py"))

        total_lines = 0
        total_classes = 0
        total_functions = 0

        for f in py_files[:200]:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                total_lines += len(content.splitlines())
                tree = ast.parse(content, filename=str(f))
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        total_classes += 1
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        total_functions += 1
            except (SyntaxError, Exception):
                continue

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "python_files": len(py_files),
                "total_lines": total_lines,
                "total_classes": total_classes,
                "total_functions": total_functions,
            },
        )
