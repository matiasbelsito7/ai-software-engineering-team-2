"""
Public API for the LLM infrastructure layer.
"""

from ai_team.infrastructure.llm.base import BaseLLM
from ai_team.infrastructure.llm.config import GenerationConfig
from ai_team.infrastructure.llm.factory import LLMFactory
from ai_team.infrastructure.llm.messages import (
    Conversation,
    Message,
    MessageRole,
)
from ai_team.infrastructure.llm.providers.ollama import OllamaLLM
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
    "Conversation",
    # Configuration
    "GenerationConfig",
    "GenerationMetadata",
    # Factory
    "LLMFactory",
    # Responses
    "LLMResponse",
    "LLMStreamChunk",
    "Message",
    # Messages
    "MessageRole",
    # Providers
    "OllamaLLM",
    "OpenRouterLLM",
    "StructuredLLMResponse",
    "TokenUsage",
]
