"""
Public API for the LLM infrastructure layer.
"""

from ai_team.infrastructure.llm.base import BaseLLM
from ai_team.infrastructure.llm.config import GenerationConfig
from ai_team.infrastructure.llm.factory import LLMFactory
from ai_team.infrastructure.llm.messages import (
    ChatMessage,
    Conversation,
    MessageRole,
)
from ai_team.infrastructure.llm.providers.openrouter import OpenRouterLLM
from ai_team.infrastructure.llm.responses import (
    GenerationMetadata,
    LLMResponse,
    LLMStreamChunk,
    StructuredLLMResponse,
    TokenUsage,
)

__all__ = [
    # Base Interface
    "BaseLLM",

    # Factory
    "LLMFactory",

    # Providers
    "OpenRouterLLM",

    # Configuration
    "GenerationConfig",

    # Messages
    "MessageRole",
    "ChatMessage",
    "Conversation",

    # Responses
    "LLMResponse",
    "StructuredLLMResponse",
    "LLMStreamChunk",
    "TokenUsage",
    "GenerationMetadata",
]