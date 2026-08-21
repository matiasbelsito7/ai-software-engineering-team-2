"""
Shared public API.

This package contains the common building blocks shared across the entire
application:

- Type aliases
- Enumerations
- Protocols
- Constants

Only stable, reusable definitions should be re-exported here.
"""

from ai_team.shared.constants import (
    API_VERSION,
    DEFAULT_ENCODING,
    DEFAULT_LLM_TIMEOUT,
    DEFAULT_MAX_CONTEXT_MESSAGES,
    DEFAULT_MAX_CONTEXT_TOKENS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_REQUEST_TIMEOUT,
    DEFAULT_RETRY_BACKOFF,
    HOURS_PER_DAY,
    MINUTES_PER_HOUR,
    PROJECT_NAME,
    PROJECT_SLUG,
    SECONDS_PER_MINUTE,
)
from ai_team.shared.protocols import (
    AgentProtocol,
    EmbeddingProtocol,
    EventBusProtocol,
    LLMProtocol,
    LoggerProtocol,
    MemoryProtocol,
    RetrieverProtocol,
    ToolProtocol,
    VectorStoreProtocol,
)
from ai_team.shared.types import (
    AgentId,
    CheckpointId,
    ConversationId,
    DocumentId,
    Embedding,
    FilePath,
    Headers,
    JSONArray,
    JSONObject,
    JSONPrimitive,
    JSONValue,
    MessageId,
    Metadata,
    Prompt,
    SessionId,
    TaskId,
    ToolArguments,
    WorkflowId,
)

__all__ = [
    "API_VERSION",
    "DEFAULT_ENCODING",
    "DEFAULT_LLM_TIMEOUT",
    "DEFAULT_MAX_CONTEXT_MESSAGES",
    "DEFAULT_MAX_CONTEXT_TOKENS",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_REQUEST_TIMEOUT",
    "DEFAULT_RETRY_BACKOFF",
    "HOURS_PER_DAY",
    "MINUTES_PER_HOUR",
    # Constants
    "PROJECT_NAME",
    "PROJECT_SLUG",
    "SECONDS_PER_MINUTE",
    "AgentId",
    "AgentProtocol",
    "CheckpointId",
    "ConversationId",
    "DocumentId",
    "Embedding",
    "EmbeddingProtocol",
    "EventBusProtocol",
    "FilePath",
    "Headers",
    "JSONArray",
    "JSONObject",
    # Types
    "JSONPrimitive",
    "JSONValue",
    # Protocols
    "LLMProtocol",
    "LoggerProtocol",
    "MemoryProtocol",
    "MessageId",
    "Metadata",
    "Prompt",
    "RetrieverProtocol",
    "SessionId",
    "TaskId",
    "ToolArguments",
    "ToolProtocol",
    "VectorStoreProtocol",
    "WorkflowId",
]
