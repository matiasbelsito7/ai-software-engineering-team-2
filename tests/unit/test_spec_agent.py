"""
Tests for the Spec Agent models.
"""

from __future__ import annotations

import pytest

from ai_team.agents.spec.models import (
    AppSpecification,
    AppComponent,
    AuthRequirements,
    DatabaseSchema,
    DBField,
    DBModel,
    DeploymentConfig,
    Endpoint,
    Feature,
    TechStack,
)


class TestSpecModels:
    """Test Spec Agent Pydantic models."""

    def test_tech_stack(self):
        stack = TechStack(frontend="React", backend="FastAPI", database="PostgreSQL")
        assert stack.frontend == "React"
        assert stack.backend == "FastAPI"

    def test_feature(self):
        feat = Feature(name="User Authentication", description="JWT-based login")
        assert feat.name == "User Authentication"
        assert feat.priority == "medium"

    def test_db_field(self):
        field = DBField(name="email", type="string")
        assert field.name == "email"
        assert field.nullable is False

    def test_db_model(self):
        model = DBModel(
            name="User",
            description="A user account",
            fields=[DBField(name="id", type="uuid")],
        )
        assert model.name == "User"
        assert len(model.fields) == 1

    def test_database_schema(self):
        schema = DatabaseSchema(models=[DBModel(name="User", description="User model")])
        assert len(schema.models) == 1

    def test_endpoint(self):
        ep = Endpoint(method="GET", path="/api/users", description="List users")
        assert ep.path == "/api/users"
        assert ep.requires_auth is False

    def test_auth_requirements(self):
        auth = AuthRequirements(required=True, method="jwt")
        assert auth.required is True
        assert auth.method == "jwt"

    def test_deployment_config(self):
        deploy = DeploymentConfig(target="docker")
        assert deploy.target == "docker"

    def test_app_component(self):
        comp = AppComponent(name="LoginForm", type="form", description="Login form")
        assert comp.name == "LoginForm"

    def test_app_specification(self):
        spec = AppSpecification(
            app_name="Todo App",
            description="A todo application",
            tech_stack=TechStack(frontend="React", backend="FastAPI", database="PostgreSQL"),
            features=[Feature(name="CRUD", description="Basic CRUD")],
            database_schema=DatabaseSchema(
                models=[DBModel(name="Todo", description="A todo item")]
            ),
            api_endpoints=[Endpoint(method="GET", path="/todos", description="List")],
        )
        assert spec.app_name == "Todo App"
        assert spec.tech_stack.frontend == "React"
        assert len(spec.features) == 1
