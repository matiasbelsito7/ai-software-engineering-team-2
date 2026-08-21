"""
Shared enumerations used throughout the project.
"""

from .agents import AgentCapability
from .database import RelationshipType
from .devops import (
    DeploymentEnvironment,
    DeploymentTarget,
    InfrastructureType,
)
from .documentation import DocumentationType
from .frontend import InteractionType, ResponsiveBreakpoint, UIComponentType
from .git import (
    GitChangeType,
    GitOperation,
)
from .llm import (
    EmbeddingProvider,
    LLMProvider,
    MessageRole,
)
from .memory import MemoryType
from .observability import ExecutionStatus, ToolType
from .qa import Severity
from .rag import EmbeddingProviderType, SourceType
from .review import (
    ReviewCategory,
    ReviewStatus,
)
from .system import (
    Environment,
    LogLevel,
    TaskStatus,
)

__all__ = [
    "AgentCapability",
    "DeploymentEnvironment",
    "DeploymentTarget",
    "DocumentationType",
    "EmbeddingProvider",
    "EmbeddingProviderType",
    "Environment",
    "ExecutionStatus",
    "GitChangeType",
    "GitOperation",
    "InfrastructureType",
    "InteractionType",
    "LLMProvider",
    "LogLevel",
    "MemoryType",
    "MessageRole",
    "RelationshipType",
    "ResponsiveBreakpoint",
    "ReviewCategory",
    "ReviewStatus",
    "Severity",
    "SourceType",
    "TaskStatus",
    "ToolType",
    "UIComponentType",
]
