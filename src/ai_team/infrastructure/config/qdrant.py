```python
"""
Qdrant configuration.

Defines the configuration required to connect to the Qdrant vector database.

This module contains configuration only.

Client creation belongs to:

    infrastructure/vector_store/
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantSettings(BaseSettings):
    """
    Qdrant vector database configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Connection
    ###########################################################################

    host: str = Field(
        default="localhost",
        description="Qdrant host.",
    )

    port: int = Field(
        default=6333,
        ge=1,
        le=65535,
        description="Qdrant REST API port.",
    )

    grpc_port: int = Field(
        default=6334,
        ge=1,
        le=65535,
        description="Qdrant gRPC port.",
    )

    use_https: bool = Field(
        default=False,
        description="Use HTTPS instead of HTTP.",
    )

    api_key: str = Field(
        default="",
        description="Qdrant Cloud API key.",
    )

    ###########################################################################
    # Collection
    ###########################################################################

    collection_name: str = Field(
        default="documents",
        description="Default vector collection.",
    )

    vector_size: int = Field(
        default=1024,
        gt=0,
        description="Embedding vector dimension.",
    )

    distance: str = Field(
        default="Cosine",
        description="Vector similarity metric.",
    )

    ###########################################################################
    # Search
    ###########################################################################

    default_top_k: int = Field(
        default=5,
        gt=0,
        description="Default retrieval size.",
    )

    score_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score.",
    )

    ###########################################################################
    # Upload
    ###########################################################################

    batch_size: int = Field(
        default=64,
        gt=0,
        description="Embedding upload batch size.",
    )

    ###########################################################################
    # Timeouts
    ###########################################################################

    timeout: int = Field(
        default=30,
        gt=0,
        description="Client timeout in seconds.",
    )

    ###########################################################################
    # URL
    ###########################################################################

    @property
    def url(self) -> str:
        """
        Return the Qdrant endpoint URL.
        """

        protocol = "https" if self.use_https else "http"

        return f"{protocol}://{self.host}:{self.port}"
```
