"""
Shared enumerations used throughout the project.
"""

from .agents import AgentCapability
from .database import RelationshipType
from .llm import (
    EmbeddingProvider,
    LLMProvider,
    MessageRole,
)
from .qa import Severity
from .review import (
    ReviewCategory,
    ReviewStatus,
)
from .system import (
    Environment,
    ExecutionStatus,
    LogLevel,
    TaskStatus,
)
from .documentation import DocumentationType
from .devops import (
    DeploymentEnvironment,
    DeploymentTarget,
    InfrastructureType,
)
from .git import (
    GitChangeType,
    GitOperation,
)
from .frontend import (
    UIComponentType,
    InteractionType,
    ResponsiveBreakpoint
)

__all__ = [
    # Agents
    "AgentCapability",

    # Database
    "RelationshipType",

    # QA
    "Severity",

    # Review
    "ReviewCategory",
    "ReviewStatus",

    # System
    "Environment",
    "TaskStatus",
    "LogLevel",
    "ExecutionStatus",

    # LLM
    "MessageRole",
    "LLMProvider",
    "EmbeddingProvider",

    # Documentation
    "DocumentationType",

    # DevOps
    "DeploymentTarget",
    "DeploymentEnvironment",
    "InfrastructureType",

    # Git
    "GitOperation",
    "GitChangeType",
    # Frontend
    "UIComponentType",
    "InteractionType",
    "ResponsiveBreakpoint"
]