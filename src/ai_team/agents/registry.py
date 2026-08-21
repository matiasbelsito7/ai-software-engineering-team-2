"""
Registry for AI agent classes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.agents.exceptions import (
    AgentNotFoundError,
    AgentRegistrationError,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from ai_team.agents.base import BaseAgent
    from ai_team.agents.info import AgentInfo
    from ai_team.shared.enums.agents import AgentCapability


class AgentRegistry:
    """
    Registry of available agent classes.
    """

    def __init__(self) -> None:
        self._registry: dict[
            AgentCapability,
            type[BaseAgent[Any]],
        ] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        agent_cls: type[BaseAgent[Any]],
    ) -> None:
        """
        Register an agent class.
        """

        capability = agent_cls.INFO.capability

        if capability in self._registry:
            raise AgentRegistrationError(
                f"Agent already registered for "
                f"{capability.value!r}"
            )

        self._registry[capability] = agent_cls

    def unregister(
        self,
        capability: AgentCapability,
    ) -> None:
        """
        Remove an agent from the registry.
        """

        try:
            del self._registry[capability]

        except KeyError as exc:
            raise AgentNotFoundError(
                f"No agent registered for "
                f"{capability.value!r}"
            ) from exc

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        capability: AgentCapability,
    ) -> type[BaseAgent[Any]]:
        """
        Return the registered agent class.
        """

        try:
            return self._registry[capability]

        except KeyError as exc:
            raise AgentNotFoundError(
                f"No agent registered for "
                f"{capability.value!r}"
            ) from exc

    def info(
        self,
        capability: AgentCapability,
    ) -> AgentInfo:
        """
        Return the metadata of a registered agent.
        """

        return self.get(capability).INFO

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def capabilities(
        self,
    ) -> tuple[AgentCapability, ...]:
        """
        Return every registered capability.
        """

        return tuple(self._registry.keys())

    def infos(
        self,
    ) -> tuple[AgentInfo, ...]:
        """
        Return metadata for every registered agent.
        """

        return tuple(
            agent.INFO
            for agent in self._registry.values()
        )

    def items(
        self,
    ) -> tuple[
        tuple[
            AgentCapability,
            type[BaseAgent[Any]],
        ],
        ...,
    ]:
        """
        Return every registry entry.
        """

        return tuple(self._registry.items())

    def clear(self) -> None:
        """
        Remove every registered agent.
        """

        self._registry.clear()

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __contains__(
        self,
        capability: AgentCapability,
    ) -> bool:
        return capability in self._registry

    def __len__(self) -> int:
        return len(self._registry)

    def __iter__(self) -> Iterator[type[BaseAgent[Any]]]:
        return iter(self._registry.values())
