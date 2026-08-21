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
