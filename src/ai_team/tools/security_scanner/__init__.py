"""
Security scanner tool.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from ai_team.tools.base import BaseTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult

_PATTERNS: list[tuple[str, str]] = [
    (r"eval\s*\(", "Use of eval()"),
    (r"exec\s*\(", "Use of exec()"),
    (r"subprocess\.call\s*\(.*shell\s*=\s*True", "Shell injection risk (shell=True)"),
    (r"os\.system\s*\(", "Use of os.system()"),
    (r"pickle\.loads?\s*\(", "Unsafe deserialization with pickle"),
    (r"__import__\s*\(", "Dynamic import"),
    (r"secret\s*=\s*['\"]", "Hardcoded secret"),
    (r"password\s*=\s*['\"]", "Hardcoded password"),
    (r"api[_-]?key\s*=\s*['\"]", "Hardcoded API key"),
    (r"SELECT\s+.*FROM\s+.*\+\s*", "Possible SQL injection"),
]


class SecurityScannerTool(BaseTool):
    """
    Scan code for security vulnerabilities.
    """

    def __init__(self) -> None:
        super().__init__(
            definition=ToolDefinition(
                name="security_scanner",
                description="Scan code for common security vulnerabilities.",
                category="security",
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
                return self._scan_file(target)
            elif target.is_dir():
                return self._scan_dir(target)
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

    def _scan_file(self, path: Path) -> ToolResult:
        content = path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()

        findings: list[dict[str, object]] = []

        for i, line in enumerate(lines, 1):
            for pattern, description in _PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        {
                            "line": i,
                            "severity": (
                                "high"
                                if "injection" in description.lower()
                                or "hardcoded" in description.lower()
                                else "medium"
                            ),
                            "description": description,
                            "code": line.strip()[:100],
                        }
                    )

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "findings": findings,
                "total_findings": len(findings),
            },
            metadata={"risk_level": self._risk_level(findings)},
        )

    def _scan_dir(self, path: Path) -> ToolResult:
        py_files = list(path.rglob("*.py"))

        all_findings: list[dict[str, object]] = []

        for f in py_files[:200]:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                lines = content.splitlines()

                for i, line in enumerate(lines, 1):
                    for pattern, description in _PATTERNS:
                        if re.search(pattern, line, re.IGNORECASE):
                            all_findings.append(
                                {
                                    "file": str(f),
                                    "line": i,
                                    "severity": (
                                        "high"
                                        if "injection" in description.lower()
                                        or "hardcoded" in description.lower()
                                        else "medium"
                                    ),
                                    "description": description,
                                }
                            )
            except Exception:
                continue

        return ToolResult(
            success=True,
            output={
                "files_scanned": len(py_files),
                "total_findings": len(all_findings),
                "findings": all_findings[:50],
            },
            metadata={"risk_level": self._risk_level(all_findings)},
        )

    def _risk_level(self, findings: list[dict[str, object]]) -> str:
        high = sum(1 for f in findings if f.get("severity") == "high")
        medium = sum(1 for f in findings if f.get("severity") == "medium")

        if high > 0:
            return "high"
        elif medium > 5:
            return "medium"
        return "low"
