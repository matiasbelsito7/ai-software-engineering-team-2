"""
Qdrant vector store implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    ScoredPoint,
    VectorParams,
)

from ai_team.rag.models import (
    DocumentChunk,
    DocumentMetadata,
    RetrievedChunk,
)
from ai_team.rag.stores.base import (
    BaseVectorStore,
)
from ai_team.shared.enums import (
    SourceType,
)

if TYPE_CHECKING:
    from ai_team.rag.embedding.base import (
        BaseEmbeddingProvider,
    )


class QdrantVectorStore(BaseVectorStore):
    """
    Qdrant implementation of the vector store.
    """

    def __init__(
        self,
        *,
        url: str,
        collection: str,
        embedding: BaseEmbeddingProvider,
        api_key: str | None = None,
        https: bool = False,
    ) -> None:
        self._collection = collection
        self._embedding = embedding

        self._client = AsyncQdrantClient(
            url=url,
            api_key=api_key,
            https=https,
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def initialize(
        self,
    ) -> None:
        """
        Create the collection if it does not exist.
        """

        collections = await self._client.get_collections()

        exists = any(collection.name == self._collection for collection in collections.collections)

        if exists:
            return

        await self._client.create_collection(
            collection_name=self._collection,
            vectors_config=VectorParams(
                size=self._embedding.dimensions,
                distance=Distance.COSINE,
            ),
        )

    async def health(
        self,
    ) -> bool:
        """
        Check whether Qdrant is available.
        """

        try:
            await self._client.get_collections()
            return True

        except Exception:
            return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _chunk_to_point(
        self,
        chunk: DocumentChunk,
    ) -> PointStruct:
        """
        Convert a DocumentChunk into a Qdrant point.
        """

        if chunk.embedding is None:
            raise ValueError("DocumentChunk has no embedding.")

        metadata = chunk.metadata

        return PointStruct(
            id=str(chunk.id),
            vector=chunk.embedding,
            payload={
                "document_id": str(chunk.document_id),
                "uri": chunk.uri,
                "source_type": chunk.source_type.value,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "title": metadata.title,
                "language": metadata.language,
                "tags": metadata.tags,
            },
        )

    def _point_to_chunk(
        self,
        point: ScoredPoint,
    ) -> RetrievedChunk:
        """
        Convert a ScoredPoint into a RetrievedChunk.
        """

        payload = point.payload or {}

        metadata = DocumentMetadata(
            title=payload.get("title"),
            language=payload.get("language"),
            tags=payload.get("tags", []),
        )

        chunk = DocumentChunk(
            id=UUID(str(point.id)),
            document_id=UUID(payload["document_id"]),
            uri=payload["uri"],
            source_type=SourceType(
                payload["source_type"],
            ),
            content=payload["content"],
            embedding=None,
            metadata=metadata,
            chunk_index=payload["chunk_index"],
        )

        return RetrievedChunk(
            chunk=chunk,
            score=point.score or 0.0,
        )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def upsert(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Insert or update document chunks.
        """

        if not chunks:
            return

        points = [self._chunk_to_point(chunk) for chunk in chunks]

        await self._client.upsert(
            collection_name=self._collection,
            points=points,
            wait=True,
        )

    async def search(
        self,
        *,
        embedding: list[float],
        limit: int,
    ) -> list[RetrievedChunk]:
        """
        Perform semantic vector search.
        """

        points = await self._client.query_points(
            collection_name=self._collection,
            query=embedding,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return [self._point_to_chunk(point) for point in points.points]

    async def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete every chunk belonging to a document.
        """

        await self._client.delete(
            collection_name=self._collection,
            points_selector={
                "filter": {
                    "must": [
                        {
                            "key": "document_id",
                            "match": {
                                "value": document_id,
                            },
                        },
                    ],
                },
            },
            wait=True,
        )

    async def clear(
        self,
    ) -> None:
        """
        Remove every indexed chunk.
        """

        exists = await self._client.collection_exists(
            self._collection,
        )

        if not exists:
            return

        await self._client.delete_collection(
            self._collection,
        )

        await self.initialize()
