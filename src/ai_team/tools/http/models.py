"""
HTTP models.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class HttpResponse:
    """
    HTTP response model.
    """

    status_code: int

    headers: dict[str, str]

    body: Any


@dataclass(slots=True)
class DownloadResult:
    """
    Downloaded content.
    """

    content: bytes

    content_type: str | None

    content_length: int | None
