"""
Browser policy.
"""

from __future__ import annotations

from urllib.parse import urlparse


class BrowserPolicy:
    """
    Validate browser operations.
    """

    BLOCKED_SCHEMES = {
        "file",
        "ftp",
    }

    def validate_url(
        self,
        url: str,
    ) -> None:

        parsed = urlparse(
            url,
        )

        if parsed.scheme not in {
            "http",
            "https",
        }:
            raise PermissionError(
                "Unsupported protocol."
            )

        if parsed.scheme in self.BLOCKED_SCHEMES:
            raise PermissionError(
                "Blocked protocol."
            )

    def validate_selector(
        self,
        selector: str,
    ) -> None:

        if not selector.strip():
            raise PermissionError(
                "Selector cannot be empty."
            )

    def validate_script(
        self,
        javascript: str,
    ) -> None:

        if not javascript.strip():
            raise PermissionError(
                "Empty JavaScript."
            )