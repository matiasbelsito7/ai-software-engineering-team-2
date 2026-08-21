"""
Unit tests for the tools subsystem.
"""

from __future__ import annotations

import pytest

from ai_team.tools.code_analyzer import CodeAnalyzerTool
from ai_team.tools.code_formatter import CodeFormatterTool
from ai_team.tools.complexity_analyzer import ComplexityAnalyzerTool
from ai_team.tools.dependency_manager import DependencyManagerTool
from ai_team.tools.documentation import DocumentationTool
from ai_team.tools.linter import LinterTool
from ai_team.tools.manager import ToolManager
from ai_team.tools.memory_tool import MemoryTool
from ai_team.tools.models import ToolDefinition, ToolRequest, ToolResult
from ai_team.tools.rag_tool import RAGTool
from ai_team.tools.repository import RepositoryTool
from ai_team.tools.search import SearchTool
from ai_team.tools.security_scanner import SecurityScannerTool
from ai_team.tools.test_runner import TestRunnerTool
from ai_team.tools.type_checker import TypeCheckerTool

# ================================================================
# ToolDefinition
# ================================================================


class TestToolDefinition:
    def test_valid_definition(self):
        d = ToolDefinition(name="test", description="A test", category="testing")
        assert d.name == "test"
        assert d.enabled is True

    def test_disabled_tool(self):
        d = ToolDefinition(name="t", description="d", category="c", enabled=False)
        assert d.enabled is False


# ================================================================
# ToolRequest / ToolResult
# ================================================================


class TestToolModels:
    def test_request_defaults(self):
        r = ToolRequest()
        assert r.tool == ""
        assert r.parameters == {}

    def test_result_success(self):
        r = ToolResult(success=True, output="ok")
        assert r.success is True
        assert r.error is None

    def test_result_failure(self):
        r = ToolResult(success=False, error="boom")
        assert r.success is False
        assert r.error == "boom"


# ================================================================
# ToolManager
# ================================================================


class TestToolManager:
    def test_register_and_get(self):
        mgr = ToolManager()
        tool = SearchTool()
        mgr.register(tool)
        assert mgr.has("search")
        assert mgr.get("search") is tool

    def test_register_duplicate_raises(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        with pytest.raises(ValueError):
            mgr.register(SearchTool())

    def test_unregister(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        mgr.unregister("search")
        assert not mgr.has("search")

    def test_names(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        mgr.register(LinterTool())
        assert "search" in mgr.names()
        assert "linter" in mgr.names()

    def test_definitions(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        defs = mgr.definitions()
        assert any(d.name == "search" for d in defs)

    def test_clear(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        mgr.clear()
        assert len(mgr) == 0

    def test_contains(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        assert "search" in mgr

    def test_iter(self):
        mgr = ToolManager()
        mgr.register(SearchTool())
        names = [t.name for t in mgr]
        assert "search" in names


# ================================================================
# Individual tool run() tests
# ================================================================


@pytest.mark.asyncio
class TestSearchTool:
    async def test_missing_query(self):
        tool = SearchTool()
        result = await tool.run(ToolRequest())
        assert result.success is False
        assert "query" in result.error

    async def test_with_query(self):
        tool = SearchTool()
        result = await tool.run(ToolRequest(parameters={"query": "python"}))
        assert result.success is True


@pytest.mark.asyncio
class TestDocumentationTool:
    async def test_read_missing_path(self):
        tool = DocumentationTool()
        result = await tool.run(ToolRequest())
        assert result.success is False

    async def test_read_nonexistent(self):
        tool = DocumentationTool()
        result = await tool.run(
            ToolRequest(parameters={"operation": "read", "path": "/nonexistent"})
        )
        assert result.success is False

    async def test_list(self):
        tool = DocumentationTool()
        result = await tool.run(ToolRequest(parameters={"operation": "list", "path": "."}))
        assert result.success is True
        assert isinstance(result.output, list)


@pytest.mark.asyncio
class TestRepositoryTool:
    async def test_list_current_dir(self):
        tool = RepositoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "list", "path": "."}))
        assert result.success is True
        assert isinstance(result.output, list)

    async def test_tree(self):
        tool = RepositoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "tree", "path": "."}))
        assert result.success is True

    async def test_info(self):
        tool = RepositoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "info", "path": "."}))
        assert result.success is True
        assert "python_files" in result.output

    async def test_unsupported_operation(self):
        tool = RepositoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "deploy", "path": "."}))
        assert result.success is False


@pytest.mark.asyncio
class TestRAGTool:
    async def test_search_missing_query(self):
        tool = RAGTool()
        result = await tool.run(ToolRequest(parameters={"operation": "search"}))
        assert result.success is False

    async def test_search(self):
        tool = RAGTool()
        result = await tool.run(ToolRequest(parameters={"operation": "search", "query": "test"}))
        assert result.success is True

    async def test_clear(self):
        tool = RAGTool()
        result = await tool.run(ToolRequest(parameters={"operation": "clear"}))
        assert result.success is True


@pytest.mark.asyncio
class TestMemoryTool:
    async def test_search_missing_query(self):
        tool = MemoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "search"}))
        assert result.success is False

    async def test_add(self):
        tool = MemoryTool()
        result = await tool.run(
            ToolRequest(parameters={"operation": "add", "content": "remember this"})
        )
        assert result.success is True

    async def test_list(self):
        tool = MemoryTool()
        result = await tool.run(ToolRequest(parameters={"operation": "list"}))
        assert result.success is True


@pytest.mark.asyncio
class TestCodeFormatterTool:
    async def test_format(self):
        tool = CodeFormatterTool()
        result = await tool.run(ToolRequest(parameters={"path": ".", "formatter": "ruff"}))
        assert result.success is True


@pytest.mark.asyncio
class TestLinterTool:
    async def test_lint(self):
        tool = LinterTool()
        result = await tool.run(ToolRequest(parameters={"path": ".", "linter": "ruff"}))
        assert result.success is True


@pytest.mark.asyncio
class TestTypeCheckerTool:
    async def test_mypy(self):
        tool = TypeCheckerTool()
        result = await tool.run(
            ToolRequest(parameters={"path": "src/ai_team/tools", "checker": "mypy"})
        )
        assert result.success is True


@pytest.mark.asyncio
class TestTestRunnerTool:
    async def test_no_tests_dir(self):
        tool = TestRunnerTool()
        result = await tool.run(ToolRequest(parameters={"path": "tests/nonexistent"}))
        assert result.success is False


@pytest.mark.asyncio
class TestDependencyManagerTool:
    async def test_list(self):
        tool = DependencyManagerTool()
        result = await tool.run(ToolRequest(parameters={"operation": "list"}))
        assert result.success is True

    async def test_freeze(self):
        tool = DependencyManagerTool()
        result = await tool.run(ToolRequest(parameters={"operation": "freeze"}))
        assert result.success is True


@pytest.mark.asyncio
class TestCodeAnalyzerTool:
    async def test_analyze_file(self):
        tool = CodeAnalyzerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools/base.py"}))
        assert result.success is True
        assert "classes" in result.output
        assert "functions" in result.output

    async def test_analyze_dir(self):
        tool = CodeAnalyzerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools"}))
        assert result.success is True
        assert "python_files" in result.output


@pytest.mark.asyncio
class TestComplexityAnalyzerTool:
    async def test_analyze_file(self):
        tool = ComplexityAnalyzerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools/base.py"}))
        assert result.success is True
        assert "cyclomatic_complexity" in result.output
        assert "rating" in result.output

    async def test_analyze_dir(self):
        tool = ComplexityAnalyzerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools"}))
        assert result.success is True
        assert "files_analyzed" in result.output


@pytest.mark.asyncio
class TestSecurityScannerTool:
    async def test_scan_file(self):
        tool = SecurityScannerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools/base.py"}))
        assert result.success is True
        assert "findings" in result.output

    async def test_scan_dir(self):
        tool = SecurityScannerTool()
        result = await tool.run(ToolRequest(parameters={"path": "src/ai_team/tools"}))
        assert result.success is True
        assert "files_scanned" in result.output
