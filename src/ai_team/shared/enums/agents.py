"""
Agent-related enumerations.
"""

from __future__ import annotations

from enum import StrEnum


class AgentCapability(StrEnum):
    """
    Capabilities supported by the agent system.
    """

    SPEC = "spec"

    PLANNER = "planner"

    ARCHITECT = "architect"

    BACKEND = "backend"

    FRONTEND = "frontend"

    DATABASE = "database"

    REVIEWER = "reviewer"

    QA = "qa"

    DOCUMENTATION = "documentation"

    DEVOPS = "devops"

    GIT = "git"
