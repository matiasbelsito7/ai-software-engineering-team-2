"""
Models used by the Spec agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ============================================================================
# Tech Stack
# ============================================================================


class TechStack(BaseModel):
    """
    Technology choices for the application.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    frontend: str = Field(
        description="Frontend framework (e.g., React, Vue, Next.js).",
    )

    backend: str = Field(
        description="Backend framework (e.g., FastAPI, Express, Django).",
    )

    database: str = Field(
        description="Database system (e.g., PostgreSQL, MongoDB, SQLite).",
    )

    styling: str | None = Field(
        default=None,
        description="CSS framework (e.g., Tailwind CSS, Bootstrap).",
    )

    extra: dict[str, str] = Field(
        default_factory=dict,
        description="Additional technology choices.",
    )


# ============================================================================
# App Component
# ============================================================================


class AppComponent(BaseModel):
    """
    A UI component or page in the application.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        description="Component name (e.g., LoginForm, DashboardPage).",
    )

    type: str = Field(
        description="Component type: page, form, modal, card, layout, nav, table.",
    )

    description: str = Field(
        description="What the component does.",
    )

    fields: list[str] = Field(
        default_factory=list,
        description="Form fields or data fields displayed.",
    )

    actions: list[str] = Field(
        default_factory=list,
        description="User actions available (e.g., submit, delete, filter).",
    )


# ============================================================================
# Feature
# ============================================================================


class Feature(BaseModel):
    """
    A business feature of the application.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        description="Feature name (e.g., user_registration, payment_processing).",
    )

    description: str = Field(
        description="What the feature does.",
    )

    priority: str = Field(
        default="medium",
        description="Priority: low, medium, high, critical.",
    )

    requires_auth: bool = Field(
        default=False,
        description="Whether this feature requires authentication.",
    )

    components: list[str] = Field(
        default_factory=list,
        description="UI components involved in this feature.",
    )


# ============================================================================
# Database Schema
# ============================================================================


class DBField(BaseModel):
    """
    A single database field.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    type: str

    nullable: bool = False

    unique: bool = False

    indexed: bool = False

    default: str | None = None

    description: str = ""


class DBModel(BaseModel):
    """
    A database model/table.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        description="Model name (e.g., User, Order, Product).",
    )

    description: str = Field(
        description="What this model represents.",
    )

    fields: list[DBField] = Field(
        default_factory=list,
    )

    relationships: list[str] = Field(
        default_factory=list,
        description="Relationship descriptions (e.g., 'has_many:orders', 'belongs_to:user').",
    )


class DatabaseSchema(BaseModel):
    """
    Complete database schema for the application.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    models: list[DBModel] = Field(
        default_factory=list,
        description="Database models/tables.",
    )

    enums: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Enum definitions (e.g., status: [active, inactive, pending]).",
    )


# ============================================================================
# API Endpoint
# ============================================================================


class Endpoint(BaseModel):
    """
    An API endpoint specification.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    method: str = Field(
        description="HTTP method: GET, POST, PUT, PATCH, DELETE.",
    )

    path: str = Field(
        description="Endpoint path (e.g., /api/users/{id}).",
    )

    description: str = Field(
        description="What this endpoint does.",
    )

    request_body: dict[str, str] | None = Field(
        default=None,
        description="Request body fields and their types.",
    )

    response_body: dict[str, str] | None = Field(
        default=None,
        description="Response body fields and their types.",
    )

    requires_auth: bool = Field(
        default=False,
        description="Whether this endpoint requires authentication.",
    )


# ============================================================================
# Auth Requirements
# ============================================================================


class AuthRequirements(BaseModel):
    """
    Authentication and authorization requirements.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    required: bool = Field(
        default=False,
        description="Whether the app requires authentication.",
    )

    method: str = Field(
        default="jwt",
        description="Auth method: jwt, session, oauth2, api_key.",
    )

    roles: list[str] = Field(
        default_factory=list,
        description="User roles (e.g., admin, user, moderator).",
    )

    features: list[str] = Field(
        default_factory=list,
        description="Auth features (e.g., registration, password_reset, email_verification).",
    )


# ============================================================================
# Deployment Config
# ============================================================================


class DeploymentConfig(BaseModel):
    """
    Deployment configuration hints.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    target: str = Field(
        default="docker",
        description="Deployment target: docker, vercel, aws, gcp, azure.",
    )

    environment_variables: list[str] = Field(
        default_factory=list,
        description="Required environment variable names.",
    )

    services: list[str] = Field(
        default_factory=list,
        description="External services needed (e.g., redis, s3, sendgrid).",
    )


# ============================================================================
# App Specification
# ============================================================================


class AppSpecification(BaseModel):
    """
    Complete technical specification for an application.

    Generated by the Spec Agent from a natural language description.
    This specification guides all downstream agents in the workflow.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    app_name: str = Field(
        description="Name of the application.",
    )

    description: str = Field(
        description="Brief description of what the app does.",
    )

    tech_stack: TechStack = Field(
        description="Technology choices.",
    )

    components: list[AppComponent] = Field(
        default_factory=list,
        description="UI components and pages.",
    )

    features: list[Feature] = Field(
        default_factory=list,
        description="Business features.",
    )

    database_schema: DatabaseSchema = Field(
        default_factory=DatabaseSchema,
        description="Database schema.",
    )

    api_endpoints: list[Endpoint] = Field(
        default_factory=list,
        description="API endpoints.",
    )

    authentication: AuthRequirements = Field(
        default_factory=AuthRequirements,
        description="Authentication requirements.",
    )

    deployment: DeploymentConfig = Field(
        default_factory=DeploymentConfig,
        description="Deployment configuration.",
    )

    complexity: str = Field(
        default="medium",
        description="App complexity: low, medium, high.",
    )

    estimated_files: int | None = Field(
        default=None,
        description="Estimated number of files to generate.",
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )
