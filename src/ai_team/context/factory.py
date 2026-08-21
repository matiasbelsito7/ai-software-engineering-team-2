"""
Context factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.context.compressor import (
    ContextCompressor,
)
from ai_team.context.manager import (
    ContextManager,
)
from ai_team.context.selector import (
    ContextSelector,
)
from ai_team.context.summarizer import (
    ContextSummarizer,
)

if TYPE_CHECKING:
    from ai_team.infrastructure.llm.base import (
        BaseLLM,
    )


def build_context(
    *,
    llm: BaseLLM,
    max_messages: int = 20,
    max_memories: int = 10,
    max_documents: int = 10,
    compress_messages: int = 15,
    compress_memories: int = 8,
    compress_documents: int = 8,
) -> ContextManager:
    """
    Build the context subsystem.

    Parameters control the selection and compression limits.
    """

    selector = ContextSelector(
        max_messages=max_messages,
        max_memories=max_memories,
        max_documents=max_documents,
    )

    compressor = ContextCompressor(
        max_messages=compress_messages,
        max_memories=compress_memories,
        max_documents=compress_documents,
    )

    summarizer = ContextSummarizer(
        llm=llm,
    )

    return ContextManager(
        selector=selector,
        compressor=compressor,
        summarizer=summarizer,
    )
