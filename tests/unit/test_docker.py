"""
Unit tests for Docker tools.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ai_team.tools.docker.docker import DockerTool
from ai_team.tools.docker.factory import build_docker_tool
from ai_team.tools.docker.manager import DockerManager
from ai_team.tools.docker.policy import DockerPolicy
from ai_team.tools.models import ToolRequest

# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock()
    client.ping.return_value = True
    client.containers.list.return_value = []
    client.images.list.return_value = []
    return client


@pytest.fixture
def manager(mock_client: MagicMock) -> DockerManager:
    return DockerManager(client=mock_client)


@pytest.fixture
def policy() -> DockerPolicy:
    return DockerPolicy()


@pytest.fixture
def tool(manager: DockerManager, policy: DockerPolicy) -> DockerTool:
    return DockerTool(manager=manager, policy=policy)


# =====================================================================
# DockerPolicy
# =====================================================================


class TestDockerPolicy:
    def test_validate_operation_valid(self, policy: DockerPolicy) -> None:
        policy.validate_operation("ping")

    def test_validate_operation_empty(self, policy: DockerPolicy) -> None:
        with pytest.raises(PermissionError, match="Operation cannot be empty"):
            policy.validate_operation("")

    def test_validate_image_valid(self, policy: DockerPolicy) -> None:
        policy.validate_image("python:3.12-slim")

    def test_validate_image_empty(self, policy: DockerPolicy) -> None:
        with pytest.raises(PermissionError, match="Image cannot be empty"):
            policy.validate_image("")

    def test_validate_image_blocked(self, policy: DockerPolicy) -> None:
        with pytest.raises(PermissionError, match="blocked"):
            policy.validate_image("docker:dind")

    def test_validate_image_blocked_custom(self) -> None:
        p = DockerPolicy(blocked_images=["evil:image"])
        with pytest.raises(PermissionError, match="blocked"):
            p.validate_image("evil:image")

    def test_validate_container_valid(self, policy: DockerPolicy) -> None:
        policy.validate_container("abc123")

    def test_validate_container_empty(self, policy: DockerPolicy) -> None:
        with pytest.raises(PermissionError, match="empty"):
            policy.validate_container("")

    def test_privileged_default(self, policy: DockerPolicy) -> None:
        assert policy.is_privileged() is False

    def test_privileged_enabled(self) -> None:
        p = DockerPolicy(privileged=True)
        assert p.is_privileged() is True

    def test_blocked_images_default(self, policy: DockerPolicy) -> None:
        assert "docker:dind" in policy._blocked
        assert "docker:latest" in policy._blocked


# =====================================================================
# DockerManager
# =====================================================================


class TestDockerManager:
    def test_ping_success(self, manager: DockerManager) -> None:
        assert manager.ping() is True

    def test_ping_failure(self, mock_client: MagicMock) -> None:
        from docker.errors import DockerException

        mock_client.ping.side_effect = DockerException("fail")
        mgr = DockerManager(client=mock_client)
        assert mgr.ping() is False

    def test_list_containers_empty(self, manager: DockerManager) -> None:
        result = manager.list_containers()
        assert result == []

    def test_list_containers_with_data(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.id = "abc123"
        container.name = "test-container"
        container.status = "running"
        container.image.tags = ["python:3.12"]

        mock_client.containers.list.return_value = [container]

        mgr = DockerManager(client=mock_client)
        result = mgr.list_containers()

        assert len(result) == 1
        assert result[0]["id"] == "abc123"
        assert result[0]["name"] == "test-container"
        assert result[0]["status"] == "running"

    def test_list_images_empty(self, manager: DockerManager) -> None:
        result = manager.list_images()
        assert result == []

    def test_start_container(self, manager: DockerManager) -> None:
        manager.start_container("abc123")

    def test_stop_container(self, manager: DockerManager) -> None:
        manager.stop_container("abc123")

    def test_remove_container(self, manager: DockerManager) -> None:
        manager.remove_container("abc123", force=True)

    def test_run_container(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.id = "new123"
        container.name = "new-container"
        mock_client.containers.run.return_value = container

        mgr = DockerManager(client=mock_client)
        result = mgr.run_container(
            image="python:3.12",
            command="echo hello",
            ports={"8000/tcp": 8000},
            environment={"ENV": "test"},
        )

        assert result["id"] == "new123"
        assert result["name"] == "new-container"

    def test_get_container_logs(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.logs.return_value = b"log line 1\nlog line 2"
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        result = mgr.get_container_logs("abc123", tail=50)

        assert "log line 1" in result
        assert "log line 2" in result

    def test_exec_in_container(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.exec_run.return_value = (0, (b"output", b""))
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        result = mgr.exec_in_container("abc123", command="ls -la")

        assert result["exit_code"] == 0
        assert "output" in result["stdout"]

    def test_inspect_container(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.attrs = {"Id": "abc123", "State": {"Status": "running"}}
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        result = mgr.inspect_container("abc123")

        assert result["Id"] == "abc123"

    def test_remove_image(self, mock_client: MagicMock) -> None:
        mgr = DockerManager(client=mock_client)
        mgr.remove_image("python:3.12")
        mock_client.images.remove.assert_called_once_with("python:3.12")

    def test_pull_image(self, mock_client: MagicMock) -> None:
        mgr = DockerManager(client=mock_client)
        mgr.pull_image("python:3.12")
        mock_client.images.pull.assert_called_once_with("python:3.12")

    def test_close(self, mock_client: MagicMock) -> None:
        mgr = DockerManager(client=mock_client)
        mgr.close()
        mock_client.close.assert_called_once()


# =====================================================================
# DockerTool
# =====================================================================


class TestDockerTool:
    async def test_ping(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "ping"})
        result = await tool.run(request)
        assert result.success is True
        assert result.output is True

    async def test_list_containers(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "list_containers"})
        result = await tool.run(request)
        assert result.success is True
        assert isinstance(result.output, list)

    async def test_list_images(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "list_images"})
        result = await tool.run(request)
        assert result.success is True
        assert isinstance(result.output, list)

    async def test_unknown_operation(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "bogus"})
        result = await tool.run(request)
        assert result.success is False
        assert "Unknown" in result.error

    async def test_blocked_image(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "pull", "image": "docker:dind"})
        result = await tool.run(request)
        assert result.success is False
        assert "blocked" in result.error

    async def test_run_container(self, mock_client: MagicMock, manager: DockerManager) -> None:
        container = MagicMock()
        container.id = "run123"
        container.name = "run-container"
        mock_client.containers.run.return_value = container

        policy = DockerPolicy()
        t = DockerTool(manager=manager, policy=policy)

        request = ToolRequest(
            parameters={
                "operation": "run",
                "image": "python:3.12",
                "command": "echo hi",
                "ports": {"8000/tcp": 8000},
                "environment": {"KEY": "val"},
            }
        )
        result = await t.run(request)
        assert result.success is True
        assert result.output["id"] == "run123"

    async def test_logs(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.logs.return_value = b"line1\nline2"
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        policy = DockerPolicy()
        t = DockerTool(manager=mgr, policy=policy)

        request = ToolRequest(parameters={"operation": "logs", "container": "abc123"})
        result = await t.run(request)
        assert result.success is True
        assert "line1" in result.output["logs"]

    async def test_exec(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.exec_run.return_value = (0, (b"ok", b""))
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        policy = DockerPolicy()
        t = DockerTool(manager=mgr, policy=policy)

        request = ToolRequest(
            parameters={
                "operation": "exec",
                "container": "abc123",
                "command": "pwd",
            }
        )
        result = await t.run(request)
        assert result.success is True
        assert result.output["exit_code"] == 0

    async def test_inspect(self, mock_client: MagicMock) -> None:
        container = MagicMock()
        container.attrs = {"Id": "abc"}
        mock_client.containers.get.return_value = container

        mgr = DockerManager(client=mock_client)
        policy = DockerPolicy()
        t = DockerTool(manager=mgr, policy=policy)

        request = ToolRequest(parameters={"operation": "inspect", "container": "abc123"})
        result = await t.run(request)
        assert result.success is True
        assert result.output["Id"] == "abc"

    async def test_remove_image(self, mock_client: MagicMock) -> None:
        mgr = DockerManager(client=mock_client)
        policy = DockerPolicy()
        t = DockerTool(manager=mgr, policy=policy)

        request = ToolRequest(parameters={"operation": "remove_image", "image": "old:latest"})
        result = await t.run(request)
        assert result.success is True

    async def test_start(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "start", "container": "abc123"})
        result = await tool.run(request)
        assert result.success is True

    async def test_stop(self, tool: DockerTool) -> None:
        request = ToolRequest(parameters={"operation": "stop", "container": "abc123"})
        result = await tool.run(request)
        assert result.success is True

    async def test_remove_container(self, tool: DockerTool) -> None:
        request = ToolRequest(
            parameters={
                "operation": "remove",
                "container": "abc123",
                "force": True,
            }
        )
        result = await tool.run(request)
        assert result.success is True


# =====================================================================
# Factory
# =====================================================================


class TestDockerFactory:
    def test_build_docker_tool(self, manager: DockerManager) -> None:
        tool = build_docker_tool(manager=manager)
        assert tool.definition.name == "docker"

    def test_build_with_custom_policy(self, manager: DockerManager) -> None:
        tool = build_docker_tool(
            manager=manager,
            blocked_images=["custom:blocked"],
            privileged=True,
        )
        assert tool.definition.name == "docker"
