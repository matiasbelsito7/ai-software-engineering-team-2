"""
Agent execution result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentResult:
    """
    Result produced by an agent execution.
    """

    success: bool

    output: Any = None

    message: str | None = None

    next_agent: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value
