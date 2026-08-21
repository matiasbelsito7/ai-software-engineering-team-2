"""
Documentation tool.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult


class DocumentationTool(BaseTool):
    """
    Read and generate project documentation.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="documentation",
                description="Read and generate project documentation.",
                category="information",
            )
        )

    async def run(self, request: ToolRequest) -> ToolResult:
        operation = request.parameters.get("operation", "read")
        path_str = request.parameters.get("path", "")

        try:
            if operation == "read":
                return self._read(path_str)
            elif operation == "list":
                return self._list(path_str)
            elif operation == "generate":
                return self._generate(request.parameters)
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

    def _read(self, path_str: str) -> ToolResult:
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

    def _list(self, path_str: str) -> ToolResult:
        root = Path(path_str) if path_str else Path()

        docs: list[str] = []

        for ext in ("*.md", "*.rst", "*.txt"):
            docs.extend(str(f) for f in root.rglob(ext))

        return ToolResult(
            success=True,
            output=docs,
            metadata={"count": len(docs)},
        )

    def _generate(self, params: dict[str, object]) -> ToolResult:
        source = str(params.get("source", ""))
        output_path = str(params.get("output", "README.md"))

        if not source:
            return ToolResult(
                success=False,
                error="Missing required parameter: source",
            )

        path = Path(source)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"Source not found: {source}",
            )

        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

        doc_lines = [f"# {path.stem}", ""]

        for line in lines[:100]:
            stripped = line.strip()
            if stripped.startswith("class "):
                doc_lines.append(f"## {stripped.split('(')[0].replace('class ', '')}")
                doc_lines.append("")
            elif stripped.startswith("def ") or stripped.startswith("async def "):
                name = stripped.split("(")[0].replace("def ", "").replace("async def ", "")
                doc_lines.append(f"- `{name}`")

        content = "\n".join(doc_lines)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")

        return ToolResult(
            success=True,
            output=content,
            metadata={"output_path": str(out)},
        )
