"""
Unit tests for the RAG subsystem.
"""

from __future__ import annotations

import pytest

from ai_team.rag.models import (
    Document,
    DocumentChunk,
    DocumentMetadata,
    DocumentSource,
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
)
from ai_team.rag.retrieval.contextual import ContextualRetriever
from ai_team.rag.retrieval.keyword import KeywordRetriever
from ai_team.rag.retrieval.reranker import RerankerRetriever
from ai_team.rag.retrieval.semantic import SemanticRetriever
from ai_team.rag.stores.memory import InMemoryVectorStore, _cosine_similarity

# ================================================================
# Models
# ================================================================


class TestDocumentModels:
    def test_document_source(self):
        from ai_team.shared.enums.rag import SourceType

        s = DocumentSource(uri="test.py", type=SourceType.PYTHON)
        assert s.uri == "test.py"

    def test_document_metadata(self):
        m = DocumentMetadata(title="test", language="python")
        assert m.title == "test"

    def test_document(self):
        from ai_team.shared.enums.rag import SourceType

        d = Document(
            source=DocumentSource(uri="x.py", type=SourceType.PYTHON),
            content="print('hi')",
            metadata=DocumentMetadata(),
        )
        assert d.content == "print('hi')"

    def test_document_chunk(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        c = DocumentChunk(
            document_id=uuid4(),
            content="chunk",
            uri="x.py",
            source_type=SourceType.PYTHON,
            metadata=DocumentMetadata(),
            chunk_index=0,
        )
        assert c.chunk_index == 0

    def test_retrieval_query(self):
        q = RetrievalQuery(query="test", top_k=3)
        assert q.top_k == 3

    def test_retrieval_result_empty(self):
        q = RetrievalQuery(query="test")
        r = RetrievalResult(query=q)
        assert r.chunks == []

    def test_rag_context(self):
        ctx = RAGContext()
        assert ctx.chunks == []
        assert ctx.summary is None


# ================================================================
# Cosine similarity
# ================================================================


class TestCosineSimilarity:
    def test_identical_vectors(self):
        assert _cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)

    def test_orthogonal_vectors(self):
        assert _cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)

    def test_opposite_vectors(self):
        assert _cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == pytest.approx(-1.0)

    def test_empty_vectors(self):
        assert _cosine_similarity([], []) == 0.0

    def test_mismatched_lengths(self):
        assert _cosine_similarity([1.0], [1.0, 2.0]) == 0.0

    def test_zero_vector(self):
        assert _cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


# ================================================================
# InMemoryVectorStore
# ================================================================


@pytest.mark.asyncio
class TestInMemoryVectorStore:
    async def test_initialize(self):
        store = InMemoryVectorStore()
        await store.initialize()

    async def test_health(self):
        store = InMemoryVectorStore()
        assert await store.health() is True

    async def test_upsert_and_search(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        store = InMemoryVectorStore()

        chunk = DocumentChunk(
            document_id=uuid4(),
            content="hello world",
            uri="test.txt",
            source_type=SourceType.FILE,
            embedding=[1.0, 0.0, 0.0],
            metadata=DocumentMetadata(),
            chunk_index=0,
        )

        await store.upsert([chunk])

        results = await store.search(embedding=[1.0, 0.0, 0.0], limit=5)
        assert len(results) == 1
        assert results[0].score == pytest.approx(1.0)

    async def test_search_no_embedding(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        store = InMemoryVectorStore()

        chunk = DocumentChunk(
            document_id=uuid4(),
            content="no embedding",
            uri="test.txt",
            source_type=SourceType.FILE,
            metadata=DocumentMetadata(),
            chunk_index=0,
        )

        await store.upsert([chunk])

        results = await store.search(embedding=[1.0, 0.0], limit=5)
        assert len(results) == 1
        assert results[0].score == 0.0

    async def test_delete(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        store = InMemoryVectorStore()
        doc_id = uuid4()

        chunk = DocumentChunk(
            document_id=doc_id,
            content="x",
            uri="t.txt",
            source_type=SourceType.FILE,
            embedding=[1.0],
            metadata=DocumentMetadata(),
            chunk_index=0,
        )

        await store.upsert([chunk])
        await store.delete(str(doc_id))

        results = await store.search(embedding=[1.0], limit=5)
        assert len(results) == 0

    async def test_clear(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        store = InMemoryVectorStore()

        chunk = DocumentChunk(
            document_id=uuid4(),
            content="x",
            uri="t.txt",
            source_type=SourceType.FILE,
            metadata=DocumentMetadata(),
            chunk_index=0,
        )

        await store.upsert([chunk])
        await store.clear()

        results = await store.search(embedding=[], limit=5)
        assert len(results) == 0

    async def test_search_empty_store(self):
        store = InMemoryVectorStore()
        results = await store.search(embedding=[1.0], limit=5)
        assert results == []


# ================================================================
# KeywordRetriever
# ================================================================


@pytest.mark.asyncio
class TestKeywordRetriever:
    async def test_empty_store(self):
        retriever = KeywordRetriever()
        result = await retriever.search(RetrievalQuery(query="test"))
        assert result.chunks == []

    async def test_build_context(self):
        retriever = KeywordRetriever()
        ctx = await retriever.build_context(RetrievalQuery(query="test"))
        assert ctx.chunks == []


# ================================================================
# SemanticRetriever
# ================================================================


class _FakeEmbeddingProvider:
    @property
    def model(self) -> str:
        return "fake"

    @property
    def dimensions(self) -> int:
        return 3

    async def embed(self, text: str) -> list[float]:
        if "hello" in text.lower():
            return [1.0, 0.0, 0.0]
        return [0.0, 1.0, 0.0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(t) for t in texts]

    async def health(self) -> bool:
        return True

    async def close(self) -> None:
        pass


@pytest.mark.asyncio
class TestSemanticRetriever:
    async def test_search(self):
        from uuid import uuid4

        from ai_team.shared.enums.rag import SourceType

        store = InMemoryVectorStore()

        chunk = DocumentChunk(
            document_id=uuid4(),
            content="hello world",
            uri="test.txt",
            source_type=SourceType.FILE,
            embedding=[1.0, 0.0, 0.0],
            metadata=DocumentMetadata(),
            chunk_index=0,
        )

        await store.upsert([chunk])

        retriever = SemanticRetriever(
            store=store,
            embedding=_FakeEmbeddingProvider(),
        )

        result = await retriever.search(RetrievalQuery(query="hello"))
        assert len(result.chunks) == 1

    async def test_build_context(self):
        retriever = SemanticRetriever(
            store=InMemoryVectorStore(),
            embedding=_FakeEmbeddingProvider(),
        )

        ctx = await retriever.build_context(RetrievalQuery(query="test"))
        assert ctx.chunks == []


# ================================================================
# RerankerRetriever
# ================================================================


@pytest.mark.asyncio
class TestRerankerRetriever:
    async def test_passthrough(self):
        base = KeywordRetriever()
        reranker = RerankerRetriever(retriever=base)
        result = await reranker.search(RetrievalQuery(query="test"))
        assert result.chunks == []


# ================================================================
# ContextualRetriever
# ================================================================


@pytest.mark.asyncio
class TestContextualRetriever:
    async def test_passthrough(self):
        base = KeywordRetriever()
        ctx_ret = ContextualRetriever(retriever=base)
        result = await ctx_ret.search(RetrievalQuery(query="test"))
        assert result.chunks == []

    async def test_with_prefix(self):
        base = KeywordRetriever()
        ctx_ret = ContextualRetriever(retriever=base, context_prefix="project: myapp")
        result = await ctx_ret.search(RetrievalQuery(query="test"))
        assert result.chunks == []
