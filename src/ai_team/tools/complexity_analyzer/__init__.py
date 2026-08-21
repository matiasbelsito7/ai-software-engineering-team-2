"""
Complexity analyzer tool.
"""

from __future__ import annotations

import ast
from pathlib import Path

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


def _cyclomatic_complexity(tree: ast.AST) -> int:
    """Estimate cyclomatic complexity from AST nodes."""

    complexity = 1

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, (ast.ExceptHandler, ast.With, ast.AsyncWith)):
            complexity += 1

    return complexity


class ComplexityAnalyzerTool(BaseTool):
    """
    Analyze code complexity metrics.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="complexity_analyzer",
                description="Analyze cyclomatic complexity and code maintainability.",
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

        try:
            tree = ast.parse(content, filename=str(path))
        except SyntaxError as exc:
            return ToolResult(
                success=False,
                error=f"Syntax error in {path}: {exc}",
            )

        complexity = _cyclomatic_complexity(tree)

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "cyclomatic_complexity": complexity,
                "rating": self._rate(complexity),
            },
        )

    def _analyze_dir(self, path: Path) -> ToolResult:
        py_files = list(path.rglob("*.py"))

        results: list[dict[str, object]] = []

        for f in py_files[:100]:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(content, filename=str(f))
                complexity = _cyclomatic_complexity(tree)
                results.append(
                    {
                        "path": str(f),
                        "complexity": complexity,
                        "rating": self._rate(complexity),
                    }
                )
            except (SyntaxError, Exception):
                continue

        results.sort(key=lambda x: int(x["complexity"]), reverse=True)  # type: ignore[call-overload]

        return ToolResult(
            success=True,
            output={
                "files_analyzed": len(results),
                "results": results[:20],
            },
        )

    def _rate(self, complexity: int) -> str:
        if complexity <= 5:
            return "A (simple)"
        elif complexity <= 10:
            return "B (moderate)"
        elif complexity <= 20:
            return "C (complex)"
        elif complexity <= 50:
            return "D (very complex)"
        return "F (extremely complex)"
