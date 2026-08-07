"""
AI agent framework.
"""

from ai_team.agents.base import BaseAgent
from ai_team.agents.context import AgentContext
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
from ai_team.agents.execution import (
    AgentExecution,
    AgentMetadata,
    AgentRequest,
    AgentStatus,
)
from ai_team.agents.factory import AgentFactory
from ai_team.agents.info import AgentInfo
from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
    PatchOperation,
)
from ai_team.agents.registry import AgentRegistry
from ai_team.agents.result import AgentResult
from ai_team.agents.review import (
    ReviewIssue,
    ReviewSeverity,
)
from ai_team.agents.tool_calls import (
    AgentToolCall,
    AgentToolResult,
)

__all__ = [

    # -----------------------------------------------------------------
    # Base
    # -----------------------------------------------------------------

    "BaseAgent",
    "AgentContext",

    # -----------------------------------------------------------------
    # Infrastructure
    # -----------------------------------------------------------------

    "AgentRegistry",
    "AgentFactory",
    "AgentDependencies",

    # -----------------------------------------------------------------
    # Execution
    # -----------------------------------------------------------------

    "AgentExecution",
    "AgentRequest",
    "AgentMetadata",
    "AgentStatus",

    # -----------------------------------------------------------------
    # Metadata
    # -----------------------------------------------------------------

    "AgentInfo",

    # -----------------------------------------------------------------
    # Result
    # -----------------------------------------------------------------

    "AgentResult",

    # -----------------------------------------------------------------
    # Tool Calling
    # -----------------------------------------------------------------

    "AgentToolCall",
    "AgentToolResult",

    # -----------------------------------------------------------------
    # Review
    # -----------------------------------------------------------------

    "ReviewIssue",
    "ReviewSeverity",

    # -----------------------------------------------------------------
    # Patches
    # -----------------------------------------------------------------

    "PatchOperation",
    "CodePatch",
    "DependencyChange",

    # -----------------------------------------------------------------
    # Exceptions
    # -----------------------------------------------------------------

    "AgentError",
    "AgentExecutionError",
    "AgentValidationError",
    "AgentConfigurationError",
    "AgentRegistrationError",
    "AgentNotFoundError",
    "AgentCapabilityError",
    "ToolExecutionError",
]