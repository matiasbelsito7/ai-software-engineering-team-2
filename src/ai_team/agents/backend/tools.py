"""
Tools available to the Backend agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class BackendTools:
    """
    Collection of tools available to the Backend agent.

    Every field is optional so the backend agent can run
    in environments where some tools are unavailable.
    """

    repository: Any | None = None

    filesystem: Any | None = None

    search: Any | None = None

    documentation: Any | None = None

    memory: Any | None = None

    rag: Any | None = None

    code_formatter: Any | None = None

    code_analyzer: Any | None = None

    dependency_manager: Any | None = None

    test_runner: Any | None = None