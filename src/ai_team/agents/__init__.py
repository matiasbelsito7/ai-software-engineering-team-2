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
    "AgentCapabilityError",
    "AgentConfigurationError",
    "AgentContext",
    "AgentDependencies",
    # -----------------------------------------------------------------
    # Exceptions
    # -----------------------------------------------------------------
    "AgentError",
    # -----------------------------------------------------------------
    # Execution
    # -----------------------------------------------------------------
    "AgentExecution",
    "AgentExecutionError",
    "AgentFactory",
    # -----------------------------------------------------------------
    # Metadata
    # -----------------------------------------------------------------
    "AgentInfo",
    "AgentMetadata",
    "AgentNotFoundError",
    "AgentRegistrationError",
    # -----------------------------------------------------------------
    # Infrastructure
    # -----------------------------------------------------------------
    "AgentRegistry",
    "AgentRequest",
    # -----------------------------------------------------------------
    # Result
    # -----------------------------------------------------------------
    "AgentResult",
    "AgentStatus",
    # -----------------------------------------------------------------
    # Tool Calling
    # -----------------------------------------------------------------
    "AgentToolCall",
    "AgentToolResult",
    "AgentValidationError",
    # -----------------------------------------------------------------
    # Base
    # -----------------------------------------------------------------
    "BaseAgent",
    "CodePatch",
    "DependencyChange",
    # -----------------------------------------------------------------
    # Patches
    # -----------------------------------------------------------------
    "PatchOperation",
    # -----------------------------------------------------------------
    # Review
    # -----------------------------------------------------------------
    "ReviewIssue",
    "ReviewSeverity",
    "ToolExecutionError",
]
