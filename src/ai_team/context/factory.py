"""
Context factory.
"""

from __future__ import annotations

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
from ai_team.llm.base import (
    BaseLLMProvider,
)


def build_context(
    *,
    llm: BaseLLMProvider,
) -> ContextManager:
    """
    Build the context subsystem.
    """

    selector = ContextSelector()

    compressor = ContextCompressor()

    summarizer = ContextSummarizer(
        llm=llm,
    )

    return ContextManager(
        selector=selector,
        compressor=compressor,
        summarizer=summarizer,
    )