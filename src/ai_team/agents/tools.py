"""
Shared tools available to AI agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class AgentTools:
    """
    Collection of tools available to AI agents.

    Every field is optional so agents can operate in
    environments where some tools are unavailable.
    """

    # =========================================================================
    # Project
    # =========================================================================

    repository: Any | None = None

    filesystem: Any | None = None

    search: Any | None = None

    # =========================================================================
    # Knowledge
    # =========================================================================

    documentation: Any | None = None

    rag: Any | None = None

    memory: Any | None = None

    # =========================================================================
    # Code Generation
    # =========================================================================

    code_formatter: Any | None = None

    dependency_manager: Any | None = None

    # =========================================================================
    # Code Analysis
    # =========================================================================

    code_analyzer: Any | None = None

    complexity_analyzer: Any | None = None

    security_scanner: Any | None = None

    # =========================================================================
    # Validation
    # =========================================================================

    test_runner: Any | None = None

    linter: Any | None = None

    type_checker: Any | None = None