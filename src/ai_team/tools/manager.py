"""
Tool manager.
"""

from __future__ import annotations

from ai_team.tools.base import BaseTool
from ai_team.tools.exceptions import ToolNotFoundError


class ToolManager:
    """
    Registry and executor for application tools.
    """

    def __init__(
        self,
        *,
        tools: list[BaseTool],
    ) -> None:

        self._tools: dict[str, BaseTool] = {
            tool.name: tool
            for tool in tools
        }

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a new tool.
        """

        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> BaseTool:
        """
        Retrieve a tool by name.
        """

        tool = self._tools.get(name)

        if tool is None:
            raise ToolNotFoundError(
                f"Tool '{name}' not found."
            )

        return tool

    def list(
        self,
    ) -> list[BaseTool]:
        """
        Return every registered tool.
        """

        return list(
            self._tools.values()
        )

    async def execute(
        self,
        *,
        tool_name: str,
        request,
    ):
        """
        Execute a registered tool.
        """

        tool = self.get(tool_name)

        return await tool.run(request)