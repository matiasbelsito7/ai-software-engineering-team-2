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
from ai_team.agents.feedback import (
    AgentFeedback,
    FeedbackRecord,
    FeedbackResponse,
    FeedbackType,
)
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
    "AgentError",
    "AgentExecution",
    "AgentExecutionError",
    "AgentFactory",
    "AgentFeedback",
    "AgentInfo",
    "AgentMetadata",
    "AgentNotFoundError",
    "AgentRegistrationError",
    "AgentRegistry",
    "AgentRequest",
    "AgentResult",
    "AgentStatus",
    "AgentToolCall",
    "AgentToolResult",
    "AgentValidationError",
    "BaseAgent",
    "CodePatch",
    "DependencyChange",
    "FeedbackRecord",
    "FeedbackResponse",
    "FeedbackType",
    "PatchOperation",
    "ReviewIssue",
    "ReviewSeverity",
    "ToolExecutionError",
]
