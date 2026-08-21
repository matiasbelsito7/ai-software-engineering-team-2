"""
Tool access policy for AI agents.
"""

from __future__ import annotations

from typing import ClassVar

from ai_team.shared.enums.agents import AgentCapability


class AgentToolPolicy:
    """
    Defines which tools each agent is allowed to use.

    This class contains authorization rules only. It does not
    execute tools or resolve tool implementations.
    """

    _POLICIES: ClassVar[dict[AgentCapability, frozenset[str]]] = {
        # =====================================================================
        # Planning
        # =====================================================================
        AgentCapability.PLANNER: frozenset(
            {
                "search",
                "documentation",
                "rag",
                "memory",
            }
        ),
        # =====================================================================
        # Architecture
        # =====================================================================
        AgentCapability.ARCHITECT: frozenset(
            {
                "search",
                "documentation",
                "rag",
                "memory",
            }
        ),
        # =====================================================================
        # Backend
        # =====================================================================
        AgentCapability.BACKEND: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "code_formatter",
                "dependency_manager",
                "code_analyzer",
                "complexity_analyzer",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
        # =====================================================================
        # Frontend
        # =====================================================================
        AgentCapability.FRONTEND: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "code_formatter",
                "dependency_manager",
                "code_analyzer",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
        # =====================================================================
        # Database
        # =====================================================================
        AgentCapability.DATABASE: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "dependency_manager",
                "code_analyzer",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
        # =====================================================================
        # Review
        # =====================================================================
        AgentCapability.REVIEWER: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "code_analyzer",
                "complexity_analyzer",
                "security_scanner",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
        # =====================================================================
        # QA
        # =====================================================================
        AgentCapability.QA: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "code_analyzer",
                "security_scanner",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
        # =====================================================================
        # Documentation
        # =====================================================================
        AgentCapability.DOCUMENTATION: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
            }
        ),
        # =====================================================================
        # DevOps
        # =====================================================================
        AgentCapability.DEVOPS: frozenset(
            {
                "repository",
                "filesystem",
                "search",
                "documentation",
                "rag",
                "memory",
                "dependency_manager",
                "code_analyzer",
                "security_scanner",
                "test_runner",
                "linter",
                "type_checker",
            }
        ),
    }

    @classmethod
    def allowed_tools(
        cls,
        capability: AgentCapability,
    ) -> frozenset[str]:
        """
        Return the tools allowed for an agent capability.
        """

        return cls._POLICIES.get(
            capability,
            frozenset(),
        )

    @classmethod
    def can_use(
        cls,
        capability: AgentCapability,
        tool_name: str,
    ) -> bool:
        """
        Return whether an agent is allowed to use a tool.
        """

        return tool_name in cls.allowed_tools(
            capability,
        )

    @classmethod
    def validate(
        cls,
        capability: AgentCapability,
        tool_name: str,
    ) -> None:
        """
        Validate tool access for an agent.

        Raises PermissionError when the requested tool is not
        allowed for the given agent capability.
        """

        if not cls.can_use(
            capability,
            tool_name,
        ):
            raise PermissionError(
                f"Agent '{capability.value}' is not allowed to use tool '{tool_name}'."
            )
