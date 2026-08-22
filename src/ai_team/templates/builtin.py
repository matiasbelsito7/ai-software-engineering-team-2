"""
Built-in task templates for common software engineering tasks.
"""

from __future__ import annotations

from ai_team.templates.models import (
    ParameterType,
    TaskTemplate,
    TemplateCategory,
    TemplateParameter,
)
from ai_team.templates.registry import TemplateRegistry


def _build_registry() -> TemplateRegistry:
    """Build registry with all built-in templates."""
    registry = TemplateRegistry()

    # =====================================================================
    # CRUD API Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="crud_api",
            name="CRUD REST API",
            description="Generate a REST API with CRUD operations for a given resource",
            category=TemplateCategory.API,
            parameters=[
                TemplateParameter(
                    name="resource_name",
                    description="Name of the resource (e.g., 'User', 'Product')",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="fields",
                    description="Comma-separated list of fields (e.g., 'name,email,age')",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="database",
                    description="Database type to use",
                    param_type=ParameterType.CHOICE,
                    default="postgresql",
                    choices=["postgresql", "mysql", "sqlite", "mongodb"],
                ),
                TemplateParameter(
                    name="auth",
                    description="Include authentication",
                    param_type=ParameterType.BOOLEAN,
                    default=True,
                ),
            ],
            task_prompt=(
                "Create a complete REST API with CRUD operations for a '{resource_name}' resource.\n\n"
                "Fields: {fields}\n"
                "Database: {database}\n"
                "Authentication: {auth}\n\n"
                "Requirements:\n"
                "- FastAPI framework\n"
                "- Pydantic models for request/response validation\n"
                "- SQLAlchemy ORM models\n"
                "- Proper error handling\n"
                "- Input validation\n"
                "- Pagination for list endpoints\n"
            ),
            tags=["api", "rest", "crud", "fastapi"],
            version="1.0.0",
            author="ai-team",
        )
    )

    # =====================================================================
    # Microservice Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="microservice",
            name="Microservice",
            description="Generate a complete microservice with Docker, health checks, and monitoring",
            category=TemplateCategory.MICROSERVICE,
            parameters=[
                TemplateParameter(
                    name="service_name",
                    description="Name of the microservice",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="port",
                    description="Port number for the service",
                    param_type=ParameterType.INTEGER,
                    default=8000,
                    min_value=1024,
                    max_value=65535,
                ),
                TemplateParameter(
                    name="features",
                    description="Comma-separated list of features (e.g., 'auth,logging,metrics')",
                    param_type=ParameterType.STRING,
                    default="logging,health",
                ),
            ],
            task_prompt=(
                "Create a complete microservice named '{service_name}'.\n\n"
                "Port: {port}\n"
                "Features: {features}\n\n"
                "Requirements:\n"
                "- FastAPI application\n"
                "- Dockerfile with multi-stage build\n"
                "- docker-compose.yml with dependencies\n"
                "- Health check endpoint\n"
                "- Structured logging\n"
                "- Graceful shutdown\n"
                "- Environment-based configuration\n"
            ),
            tags=["microservice", "docker", "fastapi"],
            version="1.0.0",
            author="ai-team",
        )
    )

    # =====================================================================
    # Data Pipeline Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="data_pipeline",
            name="Data Pipeline",
            description="Generate a data processing pipeline with ETL capabilities",
            category=TemplateCategory.DATA,
            parameters=[
                TemplateParameter(
                    name="pipeline_name",
                    description="Name of the pipeline",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="source_type",
                    description="Data source type",
                    param_type=ParameterType.CHOICE,
                    default="csv",
                    choices=["csv", "json", "api", "database"],
                ),
                TemplateParameter(
                    name="destination_type",
                    description="Data destination type",
                    param_type=ParameterType.CHOICE,
                    default="csv",
                    choices=["csv", "json", "database", "api"],
                ),
                TemplateParameter(
                    name="transformations",
                    description="Comma-separated list of transformations (e.g., 'filter,aggregate,validate')",
                    param_type=ParameterType.STRING,
                    default="validate,transform",
                ),
            ],
            task_prompt=(
                "Create a data processing pipeline named '{pipeline_name}'.\n\n"
                "Source: {source_type}\n"
                "Destination: {destination_type}\n"
                "Transformations: {transformations}\n\n"
                "Requirements:\n"
                "- Modular ETL architecture\n"
                "- Data validation at each step\n"
                "- Error handling and retry logic\n"
                "- Logging and metrics\n"
                "- Configuration via environment variables\n"
                "- Unit tests\n"
            ),
            tags=["data", "etl", "pipeline"],
            version="1.0.0",
            author="ai-team",
        )
    )

    # =====================================================================
    # CLI Tool Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="cli_tool",
            name="CLI Tool",
            description="Generate a command-line interface tool with Click or Typer",
            category=TemplateCategory.CLI,
            parameters=[
                TemplateParameter(
                    name="tool_name",
                    description="Name of the CLI tool",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="description",
                    description="Short description of the tool",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="commands",
                    description="Comma-separated list of commands (e.g., 'init,run,deploy')",
                    param_type=ParameterType.STRING,
                    default="help",
                ),
                TemplateParameter(
                    name="framework",
                    description="CLI framework to use",
                    param_type=ParameterType.CHOICE,
                    default="typer",
                    choices=["typer", "click", "argparse"],
                ),
            ],
            task_prompt=(
                "Create a CLI tool named '{tool_name}'.\n\n"
                "Description: {description}\n"
                "Commands: {commands}\n"
                "Framework: {framework}\n\n"
                "Requirements:\n"
                "- Clean command structure\n"
                "- Help text for all commands\n"
                "- Input validation\n"
                "- Error handling with user-friendly messages\n"
                "- Configuration file support\n"
                "- Installable via pip\n"
            ),
            tags=["cli", "tool", "terminal"],
            version="1.0.0",
            author="ai-team",
        )
    )

    # =====================================================================
    # Web Scraper Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="web_scraper",
            name="Web Scraper",
            description="Generate a web scraper with storage and rate limiting",
            category=TemplateCategory.WEB,
            parameters=[
                TemplateParameter(
                    name="scraper_name",
                    description="Name of the scraper",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="target_url",
                    description="Base URL to scrape",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="storage",
                    description="Storage backend for scraped data",
                    param_type=ParameterType.CHOICE,
                    default="csv",
                    choices=["csv", "json", "sqlite", "postgresql"],
                ),
                TemplateParameter(
                    name="rate_limit",
                    description="Requests per second limit",
                    param_type=ParameterType.INTEGER,
                    default=1,
                    min_value=1,
                    max_value=100,
                ),
            ],
            task_prompt=(
                "Create a web scraper named '{scraper_name}'.\n\n"
                "Target URL: {target_url}\n"
                "Storage: {storage}\n"
                "Rate Limit: {rate_limit} requests/second\n\n"
                "Requirements:\n"
                "- Async HTTP client (httpx)\n"
                "- Rate limiting\n"
                "- Retry logic with exponential backoff\n"
                "- Data extraction with CSS selectors or XPath\n"
                "- Storage backend\n"
                "- Logging and error handling\n"
                "- Configurable via environment variables\n"
            ),
            tags=["web", "scraper", "http", "async"],
            version="1.0.0",
            author="ai-team",
        )
    )

    # =====================================================================
    # Testing Suite Template
    # =====================================================================
    registry.register(
        TaskTemplate(
            template_id="testing_suite",
            name="Testing Suite",
            description="Generate a comprehensive testing suite for an existing codebase",
            category=TemplateCategory.UTILITY,
            parameters=[
                TemplateParameter(
                    name="project_name",
                    description="Name of the project to test",
                    param_type=ParameterType.STRING,
                    required=True,
                ),
                TemplateParameter(
                    name="test_types",
                    description="Comma-separated list of test types (e.g., 'unit,integration,e2e')",
                    param_type=ParameterType.STRING,
                    default="unit,integration",
                ),
                TemplateParameter(
                    name="framework",
                    description="Testing framework to use",
                    param_type=ParameterType.CHOICE,
                    default="pytest",
                    choices=["pytest", "unittest"],
                ),
            ],
            task_prompt=(
                "Create a comprehensive testing suite for '{project_name}'.\n\n"
                "Test Types: {test_types}\n"
                "Framework: {framework}\n\n"
                "Requirements:\n"
                "- Unit tests for all modules\n"
                "- Integration tests for external dependencies\n"
                "- Test fixtures and factories\n"
                "- Mocking strategy\n"
                "- Code coverage configuration\n"
                "- CI/CD integration\n"
                "- Test data management\n"
            ),
            tags=["testing", "qa", "pytest", "ci-cd"],
            version="1.0.0",
            author="ai-team",
        )
    )

    return registry


# Singleton registry instance
builtin_registry: TemplateRegistry = _build_registry()
