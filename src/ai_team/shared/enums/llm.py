"""
LLM-related enumerations.
"""

from __future__ import annotations

from enum import StrEnum


# ============================================================================
# Conversation
# ============================================================================


class MessageRole(StrEnum):
    """
    LLM message roles.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"


# ============================================================================
# Providers
# ============================================================================


class LLMProvider(StrEnum):
    """
    Supported LLM providers.
    """

    OPENROUTER = "openrouter"

    OLLAMA = "ollama"


# ============================================================================
# Embeddings
# ============================================================================


class EmbeddingProvider(StrEnum):
    """
    Supported embedding providers.
    """

    OLLAMA = "ollama"