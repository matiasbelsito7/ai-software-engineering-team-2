"""
Unit tests for the context subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock

import pytest

from ai_team.context.compressor import ContextCompressor
from ai_team.context.exceptions import (
    ContextCompressionError,
    ContextSelectionError,
    ContextSummarizationError,
)
from ai_team.context.manager import ContextManager
from ai_team.context.models import (
    ContextSelection,
    ContextSummary,
    ContextWindow,
)
from ai_team.context.selector import ContextSelector
from ai_team.context.summarizer import ContextSummarizer

# ======================================================================
# Helpers / Mocks
# ======================================================================


@dataclass
class _FakeEntry:
    content: str


@dataclass
class _FakeChunk:
    content: str


@dataclass
class _FakeConversation:
    user_request: str = "test"
    system_prompt: str | None = "You are a helpful assistant."
    conversation_history: list[str] | None = None

    def __post_init__(self) -> None:
        if self.conversation_history is None:
            self.conversation_history = []


@dataclass
class _FakeArtifact:
    results: list[Any] | None = None
    shared_files: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self.shared_files is None:
            self.shared_files = {}


@dataclass
class _FakeMemory:
    entries: list[_FakeEntry] | None = None

    def __post_init__(self) -> None:
        if self.entries is None:
            self.entries = []


@dataclass
class _FakeRAG:
    chunks: list[_FakeChunk] | None = None

    def __post_init__(self) -> None:
        if self.chunks is None:
            self.chunks = []


@dataclass
class _FakeState:
    conversation: _FakeConversation | None = None
    memory: _FakeMemory | None = None
    rag: _FakeRAG | None = None
    artifacts: _FakeArtifact | None = None

    def __post_init__(self) -> None:
        if self.conversation is None:
            self.conversation = _FakeConversation()
        if self.artifacts is None:
            self.artifacts = _FakeArtifact()


def _state(
    *,
    history: list[str] | None = None,
    system_prompt: str | None = "sys",
    memory_entries: list[str] | None = None,
    rag_chunks: list[str] | None = None,
    shared_files: dict[str, str] | None = None,
) -> _FakeState:
    conv = _FakeConversation(
        conversation_history=history or [],
        system_prompt=system_prompt,
    )
    mem = None
    if memory_entries is not None:
        mem = _FakeMemory(entries=[_FakeEntry(content=e) for e in memory_entries])

    rag = None
    if rag_chunks is not None:
        rag = _FakeRAG(chunks=[_FakeChunk(content=c) for c in rag_chunks])

    return _FakeState(
        conversation=conv,
        memory=mem,
        rag=rag,
        artifacts=_FakeArtifact(shared_files=shared_files or {}),
    )


# ======================================================================
# Models
# ======================================================================


class TestContextWindow:
    def test_defaults(self) -> None:
        w = ContextWindow()
        assert w.system_prompt is None
        assert w.conversation == []
        assert w.memory == []
        assert w.documents == []
        assert w.artifacts == {}

    def test_forbid_extra(self) -> None:
        with pytest.raises(ValueError):
            ContextWindow(foo="bar")  # type: ignore[arg-type]


class TestContextSummary:
    def test_create(self) -> None:
        s = ContextSummary(
            summary="hello",
            source_messages=10,
            compression_ratio=0.5,
        )
        assert s.summary == "hello"
        assert s.compression_ratio == 0.5


class TestContextSelection:
    def test_defaults(self) -> None:
        sel = ContextSelection()
        assert sel.conversation == []
        assert sel.memories == []
        assert sel.documents == []
        assert sel.metadata == {}


# ======================================================================
# Selector
# ======================================================================


class TestContextSelector:
    async def test_select_basic(self) -> None:
        sel = ContextSelector(max_messages=5, max_memories=3, max_documents=2)
        state = _state(
            history=[f"msg{i}" for i in range(20)],
            memory_entries=[f"mem{i}" for i in range(10)],
            rag_chunks=[f"doc{i}" for i in range(10)],
        )
        result = await sel.select(state)  # type: ignore[arg-type]
        assert len(result.conversation) == 5
        assert result.conversation[-1] == "msg19"
        assert len(result.memories) == 3
        assert len(result.documents) == 2

    async def test_select_no_memory(self) -> None:
        sel = ContextSelector()
        state = _state(history=["a", "b"])
        result = await sel.select(state)  # type: ignore[arg-type]
        assert result.conversation == ["a", "b"]
        assert result.memories == []

    async def test_select_no_rag(self) -> None:
        sel = ContextSelector()
        state = _state(history=["a"], memory_entries=["m1"])
        result = await sel.select(state)  # type: ignore[arg-type]
        assert result.documents == []


# ======================================================================
# Compressor
# ======================================================================


class TestContextCompressor:
    async def test_compress_noop(self) -> None:
        comp = ContextCompressor(max_messages=10, max_memories=5, max_documents=5)
        sel = ContextSelection(
            conversation=[f"c{i}" for i in range(5)],
            memories=[f"m{i}" for i in range(3)],
            documents=[f"d{i}" for i in range(2)],
        )
        result = await comp.compress(sel)
        assert len(result.conversation) == 5
        assert len(result.memories) == 3
        assert len(result.documents) == 2

    async def test_compress_truncates(self) -> None:
        comp = ContextCompressor(max_messages=3, max_memories=2, max_documents=1)
        sel = ContextSelection(
            conversation=[f"c{i}" for i in range(10)],
            memories=[f"m{i}" for i in range(5)],
            documents=[f"d{i}" for i in range(5)],
        )
        result = await comp.compress(sel)
        assert len(result.conversation) == 3
        assert result.conversation[-1] == "c9"
        assert len(result.memories) == 2
        assert len(result.documents) == 1

    async def test_compress_records_metadata(self) -> None:
        comp = ContextCompressor(max_messages=2, max_memories=1, max_documents=1)
        sel = ContextSelection(
            conversation=[f"c{i}" for i in range(5)],
            memories=[f"m{i}" for i in range(3)],
            documents=[f"d{i}" for i in range(4)],
        )
        result = await comp.compress(sel)
        stats = result.metadata["compression"]
        assert stats["conversation_before"] == 5
        assert stats["conversation_after"] == 2
        assert stats["total_before"] == 12
        assert stats["total_after"] == 4
        assert stats["ratio"] == pytest.approx(4 / 12)

    async def test_compress_preserves_existing_metadata(self) -> None:
        comp = ContextCompressor(max_messages=10, max_memories=5, max_documents=5)
        sel = ContextSelection(
            conversation=["c1"],
            metadata={"existing_key": "value"},
        )
        result = await comp.compress(sel)
        assert result.metadata["existing_key"] == "value"
        assert "compression" in result.metadata


# ======================================================================
# Summarizer
# ======================================================================


class TestContextSummarizer:
    async def test_summarize_empty(self) -> None:
        mock_llm = AsyncMock()
        summ = ContextSummarizer(llm=mock_llm)
        result = await summ.summarize([])
        assert result.summary == ""
        assert result.source_messages == 0
        assert result.compression_ratio == 1.0
        mock_llm.generate.assert_not_called()

    async def test_summarize_calls_llm(self) -> None:
        mock_llm = AsyncMock()
        mock_response = type("_R", (), {"content": "This is a summary."})()
        mock_llm.generate.return_value = mock_response

        summ = ContextSummarizer(llm=mock_llm)
        result = await summ.summarize(["hello", "world", "foo"])

        assert result.summary == "This is a summary."
        assert result.source_messages == 3
        assert result.compression_ratio > 0
        mock_llm.generate.assert_called_once()

    async def test_summarize_llm_error(self) -> None:
        mock_llm = AsyncMock()
        mock_llm.generate.side_effect = RuntimeError("LLM down")

        summ = ContextSummarizer(llm=mock_llm)
        with pytest.raises(ContextSummarizationError):
            await summ.summarize(["msg1", "msg2"])


# ======================================================================
# Manager
# ======================================================================


class TestContextManager:
    async def test_build_basic(self) -> None:
        selector = ContextSelector(max_messages=5, max_memories=3, max_documents=2)
        compressor = ContextCompressor(max_messages=3, max_memories=2, max_documents=1)
        mock_llm = AsyncMock()
        summarizer = ContextSummarizer(llm=mock_llm)

        mgr = ContextManager(
            selector=selector,
            compressor=compressor,
            summarizer=summarizer,
        )

        state = _state(
            history=[f"msg{i}" for i in range(10)],
            memory_entries=["memory1"],
            rag_chunks=["doc1"],
            shared_files={"file1": "content1"},
        )

        window = await mgr.build(state)  # type: ignore[arg-type]

        assert isinstance(window, ContextWindow)
        assert window.system_prompt == "sys"
        assert len(window.conversation) == 3
        assert len(window.memory) == 1
        assert len(window.documents) == 1
        assert window.artifacts == {"file1": "content1"}

    async def test_build_selection_error(self) -> None:
        selector = AsyncMock()
        selector.select.side_effect = RuntimeError("boom")
        compressor = ContextCompressor()
        mock_llm = AsyncMock()
        summarizer = ContextSummarizer(llm=mock_llm)

        mgr = ContextManager(
            selector=selector,
            compressor=compressor,
            summarizer=summarizer,
        )

        state = _state(history=["a"])
        with pytest.raises(ContextSelectionError):
            await mgr.build(state)  # type: ignore[arg-type]

    async def test_build_compression_error(self) -> None:
        selector = ContextSelector()
        compressor = AsyncMock()
        compressor.compress.side_effect = RuntimeError("boom")
        mock_llm = AsyncMock()
        summarizer = ContextSummarizer(llm=mock_llm)

        mgr = ContextManager(
            selector=selector,
            compressor=compressor,
            summarizer=summarizer,
        )

        state = _state(history=["a"])
        with pytest.raises(ContextCompressionError):
            await mgr.build(state)  # type: ignore[arg-type]

    async def test_summarize_basic(self) -> None:
        selector = ContextSelector()
        compressor = ContextCompressor()
        mock_llm = AsyncMock()
        mock_response = type("_R", (), {"content": "Summary text"})()
        mock_llm.generate.return_value = mock_response
        summarizer = ContextSummarizer(llm=mock_llm)

        mgr = ContextManager(
            selector=selector,
            compressor=compressor,
            summarizer=summarizer,
        )

        state = _state(history=["msg1", "msg2"])
        result = await mgr.summarize(state)  # type: ignore[arg-type]
        assert result == "Summary text"

    async def test_summarize_error(self) -> None:
        selector = ContextSelector()
        compressor = ContextCompressor()
        mock_llm = AsyncMock()
        mock_llm.generate.side_effect = RuntimeError("fail")
        summarizer = ContextSummarizer(llm=mock_llm)

        mgr = ContextManager(
            selector=selector,
            compressor=compressor,
            summarizer=summarizer,
        )

        state = _state(history=["msg1"])
        with pytest.raises(ContextSummarizationError):
            await mgr.summarize(state)  # type: ignore[arg-type]


# ======================================================================
# Factory
# ======================================================================


class TestContextFactory:
    def test_build_context(self) -> None:
        from ai_team.context.factory import build_context

        mock_llm = AsyncMock()
        mgr = build_context(llm=mock_llm)
        assert isinstance(mgr, ContextManager)

    def test_build_context_custom_limits(self) -> None:
        from ai_team.context.factory import build_context

        mock_llm = AsyncMock()
        mgr = build_context(
            llm=mock_llm,
            max_messages=50,
            max_memories=20,
            max_documents=20,
            compress_messages=40,
            compress_memories=15,
            compress_documents=15,
        )
        assert isinstance(mgr, ContextManager)
