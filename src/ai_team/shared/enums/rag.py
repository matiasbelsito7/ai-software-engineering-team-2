"""
Enumerations used by the RAG subsystem.
"""

from __future__ import annotations

from enum import StrEnum


class SourceType(StrEnum):
    FILE = "file"

    MARKDOWN = "markdown"

    PDF = "pdf"

    PYTHON = "python"

    GIT = "git"

    HTTP = "http"

    REPOSITORY = "repository"


class EmbeddingProviderType(StrEnum):
    """
    Supported embedding providers.
    """

    OLLAMA = "ollama"

    OPENROUTER = "openrouter"
