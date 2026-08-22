"""
Docker tool.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.tools.base import BaseTool
from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)

if TYPE_CHECKING:
    from ai_team.tools.docker.manager import DockerManager
    from ai_team.tools.docker.policy import DockerPolicy


class DockerTool(BaseTool):
    """
    High-level Docker operations.
    """

    def __init__(
        self,
        *,
        manager: DockerManager,
        policy: DockerPolicy,
    ) -> None:

        super().__init__(
            ToolDefinition(
                name="docker",
                description="Docker operations.",
                category="containers",
            ),
        )

        self._manager = manager
        self._policy = policy

    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        operation = request.parameters.get(
            "operation",
        )

        assert operation is not None

        self._policy.validate_operation(
            operation,
        )

        try:
            return self._dispatch(
                operation,
                request.parameters,
            )

        except PermissionError as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

    def _dispatch(
        self,
        operation: str,
        params: dict[str, Any],
    ) -> ToolResult:

        handlers: dict[str, Any] = {
            "ping": lambda: ToolResult(
                success=True,
                output=self._manager.ping(),
            ),
            "list_containers": lambda: ToolResult(
                success=True,
                output=self._manager.list_containers(
                    all=params.get("all", False),
                ),
            ),
            "list_images": lambda: ToolResult(
                success=True,
                output=self._manager.list_images(),
            ),
            "start": lambda: self._start(params),
            "stop": lambda: self._stop(params),
            "remove": lambda: self._remove(params),
            "pull": lambda: self._pull(params),
            "run": lambda: self._run(params),
            "logs": lambda: self._logs(params),
            "exec": lambda: self._exec(params),
            "inspect": lambda: self._inspect(params),
            "remove_image": lambda: self._remove_image(params),
        }

        handler = handlers.get(operation)

        if handler is None:
            return ToolResult(
                success=False,
                error=f"Unknown operation '{operation}'.",
            )

        return handler()  # type: ignore[no-any-return]

    # ---------------------------------------------------------
    # Container operations
    # ---------------------------------------------------------

    def _start(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        self._manager.start_container(container)

        return ToolResult(success=True)

    def _stop(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        self._manager.stop_container(container)

        return ToolResult(success=True)

    def _remove(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        self._manager.remove_container(
            container,
            force=params.get("force", False),
        )

        return ToolResult(success=True)

    def _run(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        image = params["image"]

        self._policy.validate_image(image)

        container = self._manager.run_container(
            image=image,
            command=params.get("command"),
            detach=params.get("detach", True),
            ports=params.get("ports"),
            volumes=params.get("volumes"),
            environment=params.get("environment"),
            network=params.get("network"),
            name=params.get("name"),
        )

        return ToolResult(
            success=True,
            output=container,
        )

    def _logs(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        logs = self._manager.get_container_logs(
            container,
            tail=params.get("tail", 100),
            since=params.get("since"),
        )

        return ToolResult(
            success=True,
            output={"logs": logs},
        )

    def _exec(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        result = self._manager.exec_in_container(
            container,
            command=params["command"],
            workdir=params.get("workdir"),
            user=params.get("user"),
        )

        return ToolResult(
            success=result["exit_code"] == 0,
            output=result,
        )

    def _inspect(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        container = params["container"]

        self._policy.validate_container(container)

        info = self._manager.inspect_container(container)

        return ToolResult(
            success=True,
            output=info,
        )

    # ---------------------------------------------------------
    # Image operations
    # ---------------------------------------------------------

    def _pull(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        image = params["image"]

        self._policy.validate_image(image)

        self._manager.pull_image(image)

        return ToolResult(success=True)

    def _remove_image(
        self,
        params: dict[str, Any],
    ) -> ToolResult:

        image = params["image"]

        self._policy.validate_image(image)

        self._manager.remove_image(image)

        return ToolResult(success=True)
