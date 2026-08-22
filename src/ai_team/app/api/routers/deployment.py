"""
Deployment automation router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter

from ai_team.app.api.schemas.deployment import (
    DeploymentPlanSchema,
    DeploymentRequestSchema,
    PipelineFileSchema,
)
from ai_team.deployment.generator import PipelineGenerator
from ai_team.deployment.models import (
    CICDPlatform,
    DeploymentEnvironment,
    DeploymentRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["deployment"])

_generator = PipelineGenerator()


@router.post(
    "/deployment/generate",
    response_model=DeploymentPlanSchema,
    summary="Generate deployment pipeline",
)
async def generate_deployment(
    request_body: DeploymentRequestSchema,
) -> DeploymentPlanSchema:
    """
    Generate CI/CD pipeline files for a project.
    """
    environments = None
    if request_body.environments:
        environments = [DeploymentEnvironment(e) for e in request_body.environments]

    request = DeploymentRequest(
        project_name=request_body.project_name,
        platform=CICDPlatform(request_body.platform),
        language=request_body.language,
        language_version=request_body.language_version,
        include_docker=request_body.include_docker,
        include_tests=request_body.include_tests,
        include_linting=request_body.include_linting,
        include_security=request_body.include_security,
        environments=environments,
        context=request_body.context,
    )

    plan = await _generator.generate(request)

    return DeploymentPlanSchema(
        name=plan.name,
        description=plan.description,
        platform=plan.platform,
        files=[
            PipelineFileSchema(
                file_path=f.file_path,
                content=f.content,
                platform=f.platform,
                description=f.description,
            )
            for f in plan.files
        ],
        instructions=plan.instructions,
    )
