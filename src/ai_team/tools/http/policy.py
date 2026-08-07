"""
HTTP execution policy.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


class HttpPolicy:
    """
    Validate HTTP operations before execution.
    """

    ALLOWED_SCHEMES = {
        "http",
        "https",
    }

    ALLOWED_METHODS = {
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "download",
    }

    BLOCKED_HOSTS: set[str] = set()

    # ---------------------------------------------------------

    def validate_operation(
        self,
        operation: str,
    ) -> None:

        if operation not in self.ALLOWED_METHODS:

            raise PermissionError(
                f"Unsupported HTTP operation '{operation}'."
            )

    # ---------------------------------------------------------

    def validate_url(
        self,
        url: str,
    ) -> None:

        parsed = urlparse(url)

        if parsed.scheme not in self.ALLOWED_SCHEMES:

            raise PermissionError(
                f"Unsupported scheme '{parsed.scheme}'."
            )

        if not parsed.netloc:

            raise PermissionError(
                "Invalid URL."
            )

        if parsed.hostname in self.BLOCKED_HOSTS:

            raise PermissionError(
                f"Blocked host '{parsed.hostname}'."
            )

    # ---------------------------------------------------------

    def validate_headers(
        self,
        headers: dict[str, str] | None,
    ) -> None:

        if headers is None:
            return

        if not isinstance(
            headers,
            dict,
        ):

            raise PermissionError(
                "Headers must be a dictionary."
            )

        for key, value in headers.items():

            if not isinstance(key, str):

                raise PermissionError(
                    "Header keys must be strings."
                )

            if not isinstance(value, str):

                raise PermissionError(
                    "Header values must be strings."
                )

    # ---------------------------------------------------------

    def validate_payload(
        self,
        payload: Any,
    ) -> None:

        if payload is None:
            return

        if not isinstance(
            payload,
            (
                dict,
                list,
                str,
                bytes,
            ),
        ):

            raise PermissionError(
                "Unsupported payload type."
            )