"""
Test generator - generates test files from source code.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from ai_team.testing.models import (
    TestFile,
    TestGenerationRequest,
    TestGenerationResult,
    TestSuite,
)

logger = logging.getLogger(__name__)


class TestGenerator:
    """Generates test files from source code."""

    def __init__(self) -> None:
        self._templates: dict[str, str] = {}

    async def generate(self, request: TestGenerationRequest) -> TestGenerationResult:
        """Generate tests for the provided source files."""
        suite = TestSuite(
            name="generated_tests",
            test_type=request.test_type,
            framework=request.framework,
        )

        suggestions: list[str] = []
        warnings: list[str] = []

        for file_path, content in request.source_files.items():
            test_file = await self._generate_test_file(
                file_path,
                content,
                request,
            )
            suite.files.append(test_file)

            # Analyze source for suggestions
            file_suggestions = self._analyze_source(file_path, content)
            suggestions.extend(file_suggestions)

        coverage_estimate = self._estimate_coverage(request.source_files, suite)

        if coverage_estimate < request.coverage_target:
            suggestions.append(
                f"Coverage estimate ({coverage_estimate:.0%}) is below target "
                f"({request.coverage_target:.0%}). Consider adding more tests."
            )

        logger.info(
            "Generated %d test files for %d source files",
            len(suite.files),
            len(request.source_files),
        )

        return TestGenerationResult(
            suite=suite,
            coverage_estimate=coverage_estimate,
            suggestions=suggestions,
            warnings=warnings,
        )

    async def _generate_test_file(
        self,
        source_path: str,
        content: str,
        request: TestGenerationRequest,
    ) -> TestFile:
        """Generate a test file for a single source file."""
        test_path = self._get_test_path(source_path)

        # Parse functions and classes from source
        functions = self._extract_functions(content)
        classes = self._extract_classes(content)

        # Generate test code
        test_code = self._generate_test_code(
            source_path=source_path,
            functions=functions,
            classes=classes,
            request=request,
        )

        return TestFile(
            file_path=test_path,
            content=test_code,
            test_type=request.test_type,
            framework=request.framework,
            description=f"Tests for {source_path}",
        )

    def _get_test_path(self, source_path: str) -> str:
        """Convert source path to test path."""
        parts = source_path.replace("\\", "/").split("/")
        if "src" in parts:
            idx = parts.index("src")
            parts = [*parts[:idx], "tests", *parts[idx + 1 :]]
        else:
            parts = ["tests", *parts]

        filename = parts[-1]
        filename = "test_" + filename if filename.endswith(".py") else "test_" + filename + ".py"

        parts[-1] = filename
        return "/".join(parts)

    def _extract_functions(self, content: str) -> list[dict[str, Any]]:
        """Extract function definitions from source."""
        functions = []
        pattern = r"(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*\w+)?\s*:"

        for match in re.finditer(pattern, content):
            name = match.group(1)
            params = [
                p.strip().split(":")[0].strip() for p in match.group(1).split(",") if p.strip()
            ]
            is_async = "async" in match.group(0)

            if name.startswith("_"):
                continue

            functions.append(
                {
                    "name": name,
                    "params": params,
                    "is_async": is_async,
                }
            )

        return functions

    def _extract_classes(self, content: str) -> list[dict[str, Any]]:
        """Extract class definitions from source."""
        classes = []
        pattern = r"class\s+(\w+)(?:\([^)]*\))?\s*:"

        for match in re.finditer(pattern, content):
            name = match.group(1)
            if name.startswith("_"):
                continue
            classes.append({"name": name})

        return classes

    def _generate_test_code(
        self,
        source_path: str,
        functions: list[dict[str, Any]],
        classes: list[dict[str, Any]],
        request: TestGenerationRequest,
    ) -> str:
        """Generate the test code."""
        module_name = source_path.replace("/", ".").replace("\\", ".")
        if module_name.endswith(".py"):
            module_name = module_name[:-3]

        lines = [
            '"""',
            f"Generated tests for {source_path}",
            '"""',
            "",
            "from __future__ import annotations",
            "",
            "import pytest",
            "",
            "",
        ]

        # Generate function tests
        for func in functions:
            test_name = f"test_{func['name']}"
            if func["is_async"]:
                lines.extend(
                    [
                        "@pytest.mark.asyncio",
                        f"async def {test_name}() -> None:",
                        f'    """Test {func["name"]}."""',
                        f"    # TODO: Implement test for {func['name']}",
                        "    pass",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"def {test_name}() -> None:",
                        f'    """Test {func["name"]}."""',
                        f"    # TODO: Implement test for {func['name']}",
                        "    pass",
                        "",
                    ]
                )

        # Generate class tests
        for cls in classes:
            lines.extend(
                [
                    f"class Test{cls['name']}:",
                    f'    """Tests for {cls["name"]}."""',
                    "",
                    "    def test_init(self) -> None:",
                    f'        """Test {cls["name"]} initialization."""',
                    "        # TODO: Implement initialization test",
                    "        pass",
                    "",
                ]
            )

        if not functions and not classes:
            lines.extend(
                [
                    "# No functions or classes found to test",
                    "# Add tests manually",
                    "",
                ]
            )

        return "\n".join(lines)

    def _analyze_source(self, file_path: str, content: str) -> list[str]:
        """Analyze source code and suggest test improvements."""
        suggestions = []

        # Check for error handling
        if "try:" in content and "except" in content:
            suggestions.append(f"Consider adding tests for error handling in {file_path}")

        # Check for async functions
        if "async def" in content:
            suggestions.append(f"File {file_path} has async functions - ensure async tests")

        # Check for external dependencies
        if "import requests" in content or "import httpx" in content:
            suggestions.append(f"Consider mocking HTTP calls in {file_path}")

        return suggestions

    def _estimate_coverage(
        self,
        source_files: dict[str, str],
        suite: TestSuite,
    ) -> float:
        """Estimate test coverage."""
        if not source_files:
            return 0.0

        total_functions = 0
        tested_functions = 0

        for content in source_files.values():
            functions = self._extract_functions(content)
            total_functions += len(functions)
            tested_functions += len(functions)  # All functions have test stubs

        if total_functions == 0:
            return 1.0

        return tested_functions / total_functions
