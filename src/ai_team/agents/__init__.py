"""
AI agent framework.
"""

from ai_team.agents.base import BaseAgent
from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.exceptions import (
    AgentCapabilityError,
    AgentConfigurationError,
    AgentError,
    AgentExecutionError,
    AgentNotFoundError,
    AgentRegistrationError,
    AgentValidationError,
    ToolExecutionError,
)
from ai_team.agents.factory import AgentFactory
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.registry import AgentRegistry

__all__ = [
    # Base
    "BaseAgent",

    # Infrastructure
    "AgentRegistry",
    "AgentFactory",
    "AgentDependencies",

    # Models
    "AgentInfo",
    "AgentExecution",
    "AgentResult",

    # Exceptions
    "AgentError",
    "AgentExecutionError",
    "AgentValidationError",
    "AgentConfigurationError",
    "AgentRegistrationError",
    "AgentNotFoundError",
    "AgentCapabilityError",
    "ToolExecutionError",
]