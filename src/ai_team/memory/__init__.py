"""
Memory subsystem.
"""

from ai_team.memory.manager import MemoryManager
from ai_team.memory.models import (
    MemoryContext,
    MemoryEntry,
    MemoryMetadata,
    MemoryQuery,
    MemorySearchResult,
)

from ai_team.memory.exceptions import (
    MemoryConfigurationError,
    MemoryError,
    MemoryNotFoundError,
    MemoryRetrievalError,
    MemorySerializationError,
    MemoryStoreError,
)
from ai_team.memory.factory import build_memory

__all__ = [
    # Manager
    "MemoryManager",

    # Models
    "MemoryEntry",
    "MemoryMetadata",
    "MemoryQuery",
    "MemorySearchResult",
    "MemoryContext",

    # Exceptions
    "MemoryError",
    "MemoryStoreError",
    "MemoryNotFoundError",
    "MemoryRetrievalError",
    "MemorySerializationError",
    "MemoryConfigurationError",

    # Memory factory
    "build_memory",
]