"""
Factory for creating AI agent instances.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.registry import AgentRegistry
from ai_team.shared.enums import AgentCapability


class AgentFactory:
    """
    Factory responsible for instantiating AI agents.
    """

    def __init__(
        self,
        registry: AgentRegistry,
        dependencies: AgentDependencies,
    ) -> None:
        self._registry = registry
        self._dependencies = dependencies

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def dependencies(self) -> AgentDependencies:
        return self._dependencies

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create(
        self,
        capability: AgentCapability,
    ) -> BaseAgent:
        """
        Create an agent for the requested capability.
        """

        agent_cls = self.registry.get(capability)

        return agent_cls(
            dependencies=self.dependencies,
        )

    def supports(
        self,
        capability: AgentCapability,
    ) -> bool:
        """
        Check whether a capability is registered.
        """

        return capability in self.registry

    def available_capabilities(
        self,
    ) -> tuple[AgentCapability, ...]:
        """
        Return all supported capabilities.
        """

        return self.registry.capabilities()