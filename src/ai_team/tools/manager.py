"""
Tool manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_team.tools.base import BaseTool
    from ai_team.tools.models import ToolDefinition


class ToolManager:
    """
    Registry of every available tool.
    """

    def __init__(self) -> None:

        self._tools: dict[
            str,
            BaseTool,
        ] = {}

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.
        """

        name = tool.definition.name

        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")

        self._tools[name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a tool from the registry.
        """

        self._tools.pop(
            name,
            None,
        )

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> BaseTool:
        """
        Return a tool.
        """

        try:
            return self._tools[name]

        except KeyError as exc:
            raise ValueError(f"Unknown tool '{name}'.") from exc

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Return whether a tool exists.
        """

        return name in self._tools

    def names(
        self,
    ) -> tuple[str, ...]:
        """
        Return registered tool names.
        """

        return tuple(self._tools.keys())

    def definitions(
        self,
    ) -> tuple[ToolDefinition, ...]:
        """
        Return every tool definition.
        """

        return tuple(tool.definition for tool in self._tools.values())

    def all(
        self,
    ) -> tuple[BaseTool, ...]:
        """
        Return every registered tool.
        """

        return tuple(self._tools.values())

    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove every registered tool.
        """

        self._tools.clear()

    # ---------------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.has(
            name,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._tools,
        )

    def __iter__(
        self,
    ) -> Any:

        return iter(
            self._tools.values(),
        )
