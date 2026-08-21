"""
Vector store implementations.
"""

from ai_team.rag.stores.base import BaseVectorStore
from ai_team.rag.stores.memory import InMemoryVectorStore

__all__ = [
    "BaseVectorStore",
    "InMemoryVectorStore",
]

try:
    from ai_team.rag.stores.qdrant import QdrantVectorStore

    __all__.append("QdrantVectorStore")
except ImportError:
    pass
