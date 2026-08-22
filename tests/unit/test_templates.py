"""
Unit tests for task templates.
"""

from __future__ import annotations

import pytest

from ai_team.templates.builtin import builtin_registry
from ai_team.templates.models import (
    ParameterType,
    TaskTemplate,
    TemplateCategory,
    TemplateParameter,
)
from ai_team.templates.registry import TemplateRegistry

# =====================================================================
# TemplateParameter Tests
# =====================================================================


class TestTemplateParameter:
    def test_string_parameter(self) -> None:
        param = TemplateParameter(
            name="test",
            description="Test parameter",
            param_type=ParameterType.STRING,
        )
        assert param.validate_value("hello") == "hello"
        assert param.validate_value(123) == "123"

    def test_integer_parameter(self) -> None:
        param = TemplateParameter(
            name="count",
            description="Count parameter",
            param_type=ParameterType.INTEGER,
        )
        assert param.validate_value(42) == 42
        assert param.validate_value("42") == 42

    def test_integer_with_bounds(self) -> None:
        param = TemplateParameter(
            name="port",
            description="Port number",
            param_type=ParameterType.INTEGER,
            min_value=1024,
            max_value=65535,
        )
        assert param.validate_value(8080) == 8080
        with pytest.raises(ValueError, match="must be >="):
            param.validate_value(80)
        with pytest.raises(ValueError, match="must be <="):
            param.validate_value(99999)

    def test_boolean_parameter(self) -> None:
        param = TemplateParameter(
            name="enabled",
            description="Enable feature",
            param_type=ParameterType.BOOLEAN,
        )
        assert param.validate_value(True) is True
        assert param.validate_value(False) is False
        assert param.validate_value(1) is True
        assert param.validate_value(0) is False

    def test_choice_parameter(self) -> None:
        param = TemplateParameter(
            name="color",
            description="Color choice",
            param_type=ParameterType.CHOICE,
            choices=["red", "green", "blue"],
        )
        assert param.validate_value("red") == "red"
        with pytest.raises(ValueError, match="must be one of"):
            param.validate_value("yellow")

    def test_required_parameter_no_default(self) -> None:
        param = TemplateParameter(
            name="required",
            description="Required param",
            required=True,
        )
        with pytest.raises(ValueError, match="required"):
            param.validate_value(None)

    def test_optional_parameter_with_default(self) -> None:
        param = TemplateParameter(
            name="optional",
            description="Optional param",
            required=False,
            default="default_value",
        )
        assert param.validate_value(None) == "default_value"

    def test_parameter_with_default(self) -> None:
        param = TemplateParameter(
            name="with_default",
            description="Param with default",
            default="default",
        )
        assert param.validate_value(None) == "default"


# =====================================================================
# TaskTemplate Tests
# =====================================================================


class TestTaskTemplate:
    def test_render_simple(self) -> None:
        template = TaskTemplate(
            template_id="test",
            name="Test Template",
            description="A test template",
            category=TemplateCategory.API,
            task_prompt="Create a {resource} with {fields}",
        )
        task, system_prompt = template.render({"resource": "User", "fields": "name, email"})
        assert task == "Create a User with name, email"
        assert system_prompt is None

    def test_render_with_system_prompt(self) -> None:
        template = TaskTemplate(
            template_id="test",
            name="Test Template",
            description="A test template",
            category=TemplateCategory.API,
            task_prompt="Do something",
            system_prompt="You are a {role} assistant",
        )
        task, system_prompt = template.render({"role": "coding"})
        assert task == "Do something"
        assert system_prompt == "You are a coding assistant"

    def test_render_with_parameters(self) -> None:
        template = TaskTemplate(
            template_id="test",
            name="Test Template",
            description="A test template",
            category=TemplateCategory.API,
            parameters=[
                TemplateParameter(
                    name="name",
                    description="Name",
                    param_type=ParameterType.STRING,
                ),
            ],
            task_prompt="Hello {name}",
        )
        task, _ = template.render({"name": "World"})
        assert task == "Hello World"

    def test_list_parameters(self) -> None:
        template = TaskTemplate(
            template_id="test",
            name="Test Template",
            description="A test template",
            category=TemplateCategory.API,
            parameters=[
                TemplateParameter(
                    name="param1",
                    description="First param",
                    param_type=ParameterType.STRING,
                ),
            ],
            task_prompt="Test",
        )
        params = template.list_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "param1"


# =====================================================================
# TemplateRegistry Tests
# =====================================================================


class TestTemplateRegistry:
    def test_register_and_get(self) -> None:
        registry = TemplateRegistry()
        template = TaskTemplate(
            template_id="test",
            name="Test",
            description="Test template",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        registry.register(template)
        assert registry.get("test") is template

    def test_get_nonexistent(self) -> None:
        registry = TemplateRegistry()
        assert registry.get("nonexistent") is None

    def test_unregister(self) -> None:
        registry = TemplateRegistry()
        template = TaskTemplate(
            template_id="test",
            name="Test",
            description="Test template",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        registry.register(template)
        assert registry.unregister("test") is True
        assert registry.get("test") is None

    def test_unregister_nonexistent(self) -> None:
        registry = TemplateRegistry()
        assert registry.unregister("nonexistent") is False

    def test_list_templates(self) -> None:
        registry = TemplateRegistry()
        template1 = TaskTemplate(
            template_id="api1",
            name="API 1",
            description="API template",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        template2 = TaskTemplate(
            template_id="cli1",
            name="CLI 1",
            description="CLI template",
            category=TemplateCategory.CLI,
            task_prompt="Test",
        )
        registry.register(template1)
        registry.register(template2)

        all_templates = registry.list_templates()
        assert len(all_templates) == 2

        api_templates = registry.list_templates(category="api")
        assert len(api_templates) == 1

    def test_search(self) -> None:
        registry = TemplateRegistry()
        template = TaskTemplate(
            template_id="crud",
            name="CRUD API",
            description="Generate a REST API with CRUD operations",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        registry.register(template)

        results = registry.search("crud")
        assert len(results) == 1

        results = registry.search("REST")
        assert len(results) == 1

        results = registry.search("nonexistent")
        assert len(results) == 0

    def test_render(self) -> None:
        registry = TemplateRegistry()
        template = TaskTemplate(
            template_id="test",
            name="Test",
            description="Test template",
            category=TemplateCategory.API,
            task_prompt="Hello {name}",
        )
        registry.register(template)

        task, _ = registry.render("test", {"name": "World"})
        assert task == "Hello World"

    def test_render_nonexistent(self) -> None:
        registry = TemplateRegistry()
        with pytest.raises(KeyError):
            registry.render("nonexistent", {})

    def test_count(self) -> None:
        registry = TemplateRegistry()
        assert registry.count == 0

        template = TaskTemplate(
            template_id="test",
            name="Test",
            description="Test template",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        registry.register(template)
        assert registry.count == 1

    def test_clear(self) -> None:
        registry = TemplateRegistry()
        template = TaskTemplate(
            template_id="test",
            name="Test",
            description="Test template",
            category=TemplateCategory.API,
            task_prompt="Test",
        )
        registry.register(template)
        registry.clear()
        assert registry.count == 0


# =====================================================================
# Built-in Templates Tests
# =====================================================================


class TestBuiltinTemplates:
    def test_builtin_registry_has_templates(self) -> None:
        assert builtin_registry.count > 0

    def test_crud_api_template_exists(self) -> None:
        template = builtin_registry.get("crud_api")
        assert template is not None
        assert template.name == "CRUD REST API"

    def test_microservice_template_exists(self) -> None:
        template = builtin_registry.get("microservice")
        assert template is not None
        assert template.name == "Microservice"

    def test_data_pipeline_template_exists(self) -> None:
        template = builtin_registry.get("data_pipeline")
        assert template is not None
        assert template.name == "Data Pipeline"

    def test_cli_tool_template_exists(self) -> None:
        template = builtin_registry.get("cli_tool")
        assert template is not None
        assert template.name == "CLI Tool"

    def test_web_scraper_template_exists(self) -> None:
        template = builtin_registry.get("web_scraper")
        assert template is not None
        assert template.name == "Web Scraper"

    def test_testing_suite_template_exists(self) -> None:
        template = builtin_registry.get("testing_suite")
        assert template is not None
        assert template.name == "Testing Suite"

    def test_crud_api_render(self) -> None:
        task, _system_prompt = builtin_registry.render(
            "crud_api",
            {"resource_name": "User", "fields": "name,email"},
        )
        assert "User" in task
        assert "name,email" in task

    def test_microservice_render(self) -> None:
        task, _system_prompt = builtin_registry.render(
            "microservice",
            {"service_name": "auth-service"},
        )
        assert "auth-service" in task
