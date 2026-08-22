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
    from ai_team.memory.manager import MemoryManager
    from ai_team.rag.manager import RAGManager
    from ai_team.tools.base import BaseTool


def build_tools(
    *,
    workspace: Workspace,
    rag: RAGManager | None = None,
    memory: MemoryManager | None = None,
) -> ToolManager:
    """
    Build the application tool registry.
    """

    terminal = TerminalTool(
        workspace=workspace,
    )

    tools: list[BaseTool] = [
        # Core tools
        FilesystemTool(workspace=workspace),
        terminal,
        GitTool(terminal=terminal),
        PythonTool(terminal=terminal),
        # Information tools
        SearchTool(),
        DocumentationTool(),
        RepositoryTool(),
        RAGTool(rag=rag),
        MemoryTool(memory=memory),
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

    # Register optional tools that may not be available
    _register_optional_tools(tool_manager)

    return tool_manager


def _register_optional_tools(tool_manager: ToolManager) -> None:
    """Register tools that depend on optional packages."""

    try:
        import docker

        from ai_team.tools.docker.factory import build_docker_tool
        from ai_team.tools.docker.manager import DockerManager

        client = docker.from_env()
        docker_manager = DockerManager(client=client)
        docker_tool = build_docker_tool(manager=docker_manager)
        tool_manager.register(docker_tool)
    except Exception:
        pass

    try:
        import httpx

        from ai_team.tools.http.factory import build_http_tool
        from ai_team.tools.http.manager import HttpManager

        client = httpx.AsyncClient()
        http_manager = HttpManager(client=client)
        http_tool = build_http_tool(manager=http_manager)
        tool_manager.register(http_tool)
    except Exception:
        pass

    try:
        from ai_team.tools.browser.factory import build_browser_tool
        from ai_team.tools.browser.manager import BrowserManager

        browser_manager = BrowserManager()
        browser_tool = build_browser_tool(manager=browser_manager)
        tool_manager.register(browser_tool)
    except Exception:
        pass
