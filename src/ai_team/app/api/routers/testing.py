"""
Testing pipeline router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter

from ai_team.app.api.schemas.testing import (
    TestFileSchema,
    TestGenerationRequestSchema,
    TestGenerationResultSchema,
    TestSuiteSchema,
)
from ai_team.testing.generator import TestGenerator
from ai_team.testing.models import TestFramework, TestGenerationRequest, TestType

logger = logging.getLogger(__name__)

router = APIRouter(tags=["testing"])

_generator = TestGenerator()


@router.post(
    "/tests/generate",
    response_model=TestGenerationResultSchema,
    summary="Generate tests for source code",
)
async def generate_tests(
    request_body: TestGenerationRequestSchema,
) -> TestGenerationResultSchema:
    """
    Generate test files from source code.
    """
    request = TestGenerationRequest(
        source_files=request_body.source_files,
        test_type=TestType(request_body.test_type),
        framework=TestFramework(request_body.framework),
        coverage_target=request_body.coverage_target,
        include_fixtures=request_body.include_fixtures,
        include_mocks=request_body.include_mocks,
        context=request_body.context,
    )

    result = await _generator.generate(request)

    return TestGenerationResultSchema(
        suite=TestSuiteSchema(
            name=result.suite.name,
            description=result.suite.description,
            files=[
                TestFileSchema(
                    file_path=f.file_path,
                    content=f.content,
                    test_type=f.test_type,
                    framework=f.framework,
                    description=f.description,
                )
                for f in result.suite.files
            ],
            test_type=result.suite.test_type,
            framework=result.suite.framework,
            file_count=result.suite.file_count,
        ),
        coverage_estimate=result.coverage_estimate,
        suggestions=result.suggestions,
        warnings=result.warnings,
    )
