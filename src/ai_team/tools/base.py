"""
Base tool abstraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai_team.tools.models import (
    ToolDefinition,
    ToolRequest,
    ToolResult,
)


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    def __init__(
        self,
        definition: ToolDefinition,
    ) -> None:

        self._definition = definition

    @property
    def definition(
        self,
    ) -> ToolDefinition:
        """
        Tool metadata.
        """

        return self._definition

    @property
    def name(
        self,
    ) -> str:

        return self._definition.name

    @property
    def description(
        self,
    ) -> str:

        return self._definition.description

    @property
    def category(
        self,
    ) -> str:

        return self._definition.category

    @abstractmethod
    async def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Execute the tool.
        """

        raise NotImplementedError