"""
Enumerations used by the observability subsystem.
"""

from __future__ import annotations

from enum import StrEnum


class LLMProvider(StrEnum):
    """
    Supported LLM providers.
    """

    OPENROUTER = "openrouter"

    OLLAMA = "ollama"


class ToolType(StrEnum):
    """
    Supported tool categories.
    """

    RAG = "rag"

    MEMORY = "memory"

    SANDBOX = "sandbox"

    GIT = "git"

    FILESYSTEM = "filesystem"

    API = "api"


class ExecutionStatus(StrEnum):
    """
    Agent execution status.
    """

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"
