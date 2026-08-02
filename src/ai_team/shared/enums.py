```python
"""
Shared enumerations used across the AI Software Engineering Team project.

Only globally shared enums belong here.

Module-specific enums should live inside their corresponding package.
"""

from __future__ import annotations

from enum import Enum, StrEnum, auto


###############################################################################
# Environment
###############################################################################


class Environment(StrEnum):
    """Application runtime environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


###############################################################################
# Agent Roles
###############################################################################


class AgentRole(StrEnum):
    """Available agent roles."""

    PLANNER = "planner"
    ARCHITECT = "architect"
    CODER = "coder"
    REVIEWER = "reviewer"
    QA = "qa"
    DEVOPS = "devops"
    DOCUMENTATION = "documentation"


###############################################################################
# Workflow / Tasks
###############################################################################


class TaskStatus(StrEnum):
    """Task lifecycle."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


###############################################################################
# Conversation
###############################################################################


class MessageRole(StrEnum):
    """LLM message roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


###############################################################################
# LLM Providers
###############################################################################


class LLMProvider(StrEnum):
    """Supported LLM providers."""

    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


###############################################################################
# Memory
###############################################################################


class MemoryType(StrEnum):
    """Memory layers."""

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    PROJECT = "project"


###############################################################################
# Tools
###############################################################################


class ToolCategory(StrEnum):
    """High-level tool categories."""

    FILESYSTEM = "filesystem"
    GIT = "git"
    SEARCH = "search"
    SANDBOX = "sandbox"
    HTTP = "http"
    PYTHON = "python"


###############################################################################
# Vector Store
###############################################################################


class VectorStore(StrEnum):
    """Supported vector databases."""

    QDRANT = "qdrant"


###############################################################################
# Embedding Providers
###############################################################################


class EmbeddingProvider(StrEnum):
    """Embedding providers."""

    OLLAMA = "ollama"


###############################################################################
# Logging
###############################################################################


class LogLevel(StrEnum):
    """Application log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


###############################################################################
# Execution Result
###############################################################################


class ExecutionStatus(Enum):
    """Generic execution outcome."""

    SUCCESS = auto()
    FAILURE = auto()
    RETRY = auto()
```


# ============================================================================
# Enums
# ============================================================================


class AgentCapability(StrEnum):
    """
    Capabilities supported by the agent system.
    """

    PLANNING = "planning"
    ARCHITECTURE = "architecture"
    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"
    REVIEW = "review"
    QA = "qa"
    DOCUMENTATION = "documentation"
    DEVOPS = "devops"
    GIT = "git"