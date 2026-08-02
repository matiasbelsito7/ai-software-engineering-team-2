"""
Tools available to the Planner agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class PlannerTools:
    """
    Collection of tools available to the Planner agent.

    Every field is optional so the planner can run in
    environments where some tools are unavailable.
    """

    repository: Any | None = None

    filesystem: Any | None = None

    documentation: Any | None = None

    search: Any | None = None

    memory: Any | None = None

    rag: Any | None = None