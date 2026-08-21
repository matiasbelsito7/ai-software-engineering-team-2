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
    from collections.abc import Callable

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

        self._operations: dict[
            str,
            Callable[[dict[str, Any]], ToolResult],
        ] = {
            "ping": lambda _: ToolResult(
                success=True,
                output=self._manager.ping(),
            ),
            "list_containers": lambda p: ToolResult(
                success=True,
                output=self._manager.list_containers(
                    all=p.get("all", False),
                ),
            ),
            "list_images": lambda _: ToolResult(
                success=True,
                output=self._manager.list_images(),
            ),
            "start": self._start,
            "stop": self._stop,
            "remove": self._remove,
            "pull": self._pull,
            "run": self._run,
        }

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

        handler = self._operations.get(
            operation,
        )

        if handler is None:
            return ToolResult(
                success=False,
                error=f"Unknown operation '{operation}'.",
            )

        try:
            return handler(
                request.parameters,
            )

        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

    # ---------------------------------------------------------

    def _start(
        self,
        parameters: dict[str, Any],
    ) -> ToolResult:

        container = parameters["container"]

        self._policy.validate_container(
            container,
        )

        self._manager.start_container(
            container,
        )

        return ToolResult(
            success=True,
        )

    def _stop(
        self,
        parameters: dict[str, Any],
    ) -> ToolResult:

        container = parameters["container"]

        self._policy.validate_container(
            container,
        )

        self._manager.stop_container(
            container,
        )

        return ToolResult(
            success=True,
        )

    def _remove(
        self,
        parameters: dict[str, Any],
    ) -> ToolResult:

        container = parameters["container"]

        self._policy.validate_container(
            container,
        )

        self._manager.remove_container(
            container,
            force=parameters.get(
                "force",
                False,
            ),
        )

        return ToolResult(
            success=True,
        )

    def _pull(
        self,
        parameters: dict[str, Any],
    ) -> ToolResult:

        image = parameters["image"]

        self._policy.validate_image(
            image,
        )

        self._manager.pull_image(
            image,
        )

        return ToolResult(
            success=True,
        )

    def _run(
        self,
        parameters: dict[str, Any],
    ) -> ToolResult:

        image = parameters["image"]

        self._policy.validate_image(
            image,
        )

        container = self._manager.run_container(
            image=image,
            command=parameters.get(
                "command",
            ),
            detach=parameters.get(
                "detach",
                True,
            ),
        )

        return ToolResult(
            success=True,
            output=container,
        )
