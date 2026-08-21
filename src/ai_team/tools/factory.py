"""
Tool factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.tools.code_analyzer import CodeAnalyzerTool
from ai_team.tools.code_formatter import CodeFormatterTool
from ai_team.tools.complexity_analyzer import ComplexityAnalyzerTool
from ai_team.tools.dependency_manager import DependencyManagerTool
from ai_team.tools.documentation import DocumentationTool
from ai_team.tools.filesystem import FilesystemTool
from ai_team.tools.git import GitTool
from ai_team.tools.linter import LinterTool
from ai_team.tools.manager import ToolManager
from ai_team.tools.memory_tool import MemoryTool
from ai_team.tools.python import PythonTool
from ai_team.tools.rag_tool import RAGTool
from ai_team.tools.repository import RepositoryTool
from ai_team.tools.search import SearchTool
from ai_team.tools.security_scanner import SecurityScannerTool
from ai_team.tools.terminal import TerminalTool
from ai_team.tools.test_runner import TestRunnerTool
from ai_team.tools.type_checker import TypeCheckerTool

if TYPE_CHECKING:
    from ai_team.infrastructure.workspace import Workspace


def build_tools(
    *,
    workspace: Workspace,
) -> ToolManager:
    """
    Build the application tool registry.
    """

    terminal = TerminalTool(
        workspace=workspace,
    )

    tools = [
        # Core tools
        FilesystemTool(workspace=workspace),
        terminal,
        GitTool(terminal=terminal),
        PythonTool(terminal=terminal),
        # Information tools
        SearchTool(),
        DocumentationTool(),
        RepositoryTool(),
        RAGTool(),
        MemoryTool(),
        # Code quality tools
        CodeFormatterTool(),
        CodeAnalyzerTool(),
        ComplexityAnalyzerTool(),
        LinterTool(),
        TypeCheckerTool(),
        TestRunnerTool(),
        SecurityScannerTool(),
        DependencyManagerTool(),
    ]

    tool_manager = ToolManager()

    for tool in tools:
        tool_manager.register(tool)

    return tool_manager
