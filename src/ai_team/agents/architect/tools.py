"""
Tools available to the Architect agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class ArchitectTools:
    """
    Collection of tools available to the Architect agent.

    Every field is optional so the architect can run in
    environments where some tools are unavailable.
    """

    repository: Any | None = None

    filesystem: Any | None = None

    documentation: Any | None = None

    search: Any | None = None

    memory: Any | None = None

    rag: Any | None = None

    dependency_graph: Any | None = None

    architecture_analyzer: Any | None = None