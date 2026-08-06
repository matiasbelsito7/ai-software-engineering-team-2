"""
Browser models.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class BrowserSession:
    """
    Browser session identifier.
    """

    id: UUID