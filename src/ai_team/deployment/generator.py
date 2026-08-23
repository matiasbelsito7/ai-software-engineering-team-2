"""
Pipeline generator - generates CI/CD pipeline files.
"""

from __future__ import annotations

import logging

from ai_team.deployment.models import (
    CICDPlatform,
    DeploymentEnvironment,
    DeploymentPlan,
    DeploymentRequest,
    PipelineConfig,
    PipelineFile,
)

logger = logging.getLogger(__name__)


class PipelineGenerator:
    """Generates CI/CD pipeline files."""

    async def generate(self, request: DeploymentRequest) -> DeploymentPlan:
        """Generate deployment pipeline files."""
        config = PipelineConfig(
            platform=request.platform,
            project_name=request.project_name,
            language=request.language,
            language_version=request.language_version,
            environments=request.environments
            or [
                DeploymentEnvironment.DEVELOPMENT,
                DeploymentEnvironment.STAGING,
            ],
        )

        files: list[PipelineFile] = []

        if request.platform == CICDPlatform.GITHUB_ACTIONS:
            files.extend(self._generate_github_actions(config, request))
        elif request.platform == CICDPlatform.GITLAB_CI:
            files.extend(self._generate_gitlab_ci(config, request))

        if request.include_docker:
            files.extend(self._generate_docker_files(config))

        instructions = self._generate_instructions(request)

        plan = DeploymentPlan(
            name=f"{request.project_name}-deployment",
            description=f"Deployment pipeline for {request.project_name}",
            platform=request.platform,
            files=files,
            instructions=instructions,
            metadata={
                "project_name": request.project_name,
                "language": request.language,
                "platform": request.platform,
            },
        )

        logger.info(
            "Generated deployment plan with %d files for %s",
            len(files),
            request.project_name,
        )

        return plan

    def _generate_github_actions(
        self,
        config: PipelineConfig,
        request: DeploymentRequest,
    ) -> list[PipelineFile]:
        """Generate GitHub Actions workflow files."""
        files = []

        # Main CI/CD workflow
        workflow_content = self._build_github_workflow(config, request)
        files.append(
            PipelineFile(
                file_path=".github/workflows/ci.yml",
                content=workflow_content,
                platform=CICDPlatform.GITHUB_ACTIONS,
                description="Main CI/CD workflow",
            )
        )

        # Deploy workflow
        deploy_content = self._build_github_deploy(config, request)
        files.append(
            PipelineFile(
                file_path=".github/workflows/deploy.yml",
                content=deploy_content,
                platform=CICDPlatform.GITHUB_ACTIONS,
                description="Deployment workflow",
            )
        )

        return files

    def _build_github_workflow(
        self,
        config: PipelineConfig,
        request: DeploymentRequest,
    ) -> str:
        """Build GitHub Actions CI workflow."""
        steps = []

        steps.append("      - uses: actions/checkout@v4")
        steps.append("      - uses: actions/setup-python@v5")
        steps.append("        with:")
        steps.append(f"          python-version: '{config.language_version}'")

        if request.include_linting:
            steps.extend(
                [
                    "      - name: Install dependencies",
                    "        run: |",
                    "          python -m pip install --upgrade pip",
                    "          pip install ruff mypy",
                    "      - name: Lint with ruff",
                    "        run: ruff check .",
                    "      - name: Type check with mypy",
                    "        run: mypy src/",
                ]
            )

        if request.include_tests:
            steps.extend(
                [
                    "      - name: Install test dependencies",
                    "        run: pip install pytest pytest-cov",
                    "      - name: Run tests",
                    "        run: pytest tests/ --cov=src --cov-report=xml",
                ]
            )

        if request.include_security:
            steps.extend(
                [
                    "      - name: Security scan",
                    "        run: |",
                    "          pip install safety bandit",
                    "          safety check",
                    "          bandit -r src/",
                ]
            )

        workflow = f"""name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
{chr(10).join(steps)}
"""
        return workflow

    def _build_github_deploy(
        self,
        config: PipelineConfig,
        request: DeploymentRequest,
    ) -> str:
        """Build GitHub Actions deploy workflow."""
        environments = config.environments or [DeploymentEnvironment.STAGING]

        env_configs = [f"""  {env.value}:
    runs-on: ubuntu-latest
    needs: ci
    if: github.ref == 'refs/heads/main'
    environment: {env.value}
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to {env.value}
        run: echo "Deploying to {env.value}..."
""" for env in environments]

        workflow = f"""name: Deploy

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
  push:
    branches: [main]

jobs:
{chr(10).join(env_configs)}"""
        return workflow

    def _generate_gitlab_ci(
        self,
        config: PipelineConfig,
        request: DeploymentRequest,
    ) -> list[PipelineFile]:
        """Generate GitLab CI files."""
        content = """stages:
  - lint
  - test
  - security
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install --upgrade pip

"""
        if request.include_linting:
            content += """lint:
  stage: lint
  script:
    - pip install ruff mypy
    - ruff check .
    - mypy src/

"""

        if request.include_tests:
            content += """test:
  stage: test
  script:
    - pip install pytest pytest-cov
    - pytest tests/ --cov=src --cov-report=xml

"""

        if request.include_security:
            content += """security:
  stage: security
  script:
    - pip install safety bandit
    - safety check
    - bandit -r src/

"""

        return [
            PipelineFile(
                file_path=".gitlab-ci.yml",
                content=content,
                platform=CICDPlatform.GITLAB_CI,
                description="GitLab CI pipeline",
            )
        ]

    def _generate_docker_files(self, config: PipelineConfig) -> list[PipelineFile]:
        """Generate Docker-related files."""
        files = []

        dockerfile = f"""FROM python:{config.language_version}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        files.append(
            PipelineFile(
                file_path="Dockerfile",
                content=dockerfile,
                platform=CICDPlatform.GITHUB_ACTIONS,
                description="Docker image definition",
            )
        )

        docker_compose = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./workspace:/app/workspace
"""
        files.append(
            PipelineFile(
                file_path="docker-compose.yml",
                content=docker_compose,
                platform=CICDPlatform.GITHUB_ACTIONS,
                description="Docker Compose configuration",
            )
        )

        return files

    def _generate_instructions(self, request: DeploymentRequest) -> str:
        """Generate deployment instructions."""
        instructions = f"""# Deployment Instructions for {request.project_name}

## Prerequisites
- Python {request.language_version}
- Docker (if using containerized deployment)

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables

## CI/CD Pipeline
The pipeline will automatically:
"""

        if request.include_linting:
            instructions += "- Run code linting with ruff\n"
        if request.include_tests:
            instructions += "- Execute test suite\n"
        if request.include_security:
            instructions += "- Perform security scans\n"
        if request.include_docker:
            instructions += "- Build and push Docker images\n"

        instructions += """
## Deployment
1. Push to main branch triggers automatic deployment
2. Staging environment deploys first
3. Production deployment requires manual approval

## Environment Variables
Configure the following in your CI/CD platform:
- DATABASE_URL
- API_KEY
- SECRET_KEY
"""

        return instructions
