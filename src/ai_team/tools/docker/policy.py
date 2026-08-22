"""
Docker execution policy.
"""

from __future__ import annotations

from typing import ClassVar


class DockerPolicy:
    """
    Validate Docker operations.
    """

    BLOCKED_IMAGES: ClassVar[set[str]] = {
        "docker:dind",
        "docker:latest",
    }

    def __init__(
        self,
        *,
        blocked_images: list[str] | None = None,
        privileged: bool = False,
    ) -> None:

        self._blocked = self.BLOCKED_IMAGES.copy()

        if blocked_images is not None:
            self._blocked.update(blocked_images)

        self._privileged = privileged

    def validate_operation(
        self,
        operation: str,
    ) -> None:

        if not operation:
            raise PermissionError("Operation cannot be empty.")

    def validate_image(
        self,
        image: str,
    ) -> None:

        if not image:
            raise PermissionError("Image cannot be empty.")

        if image in self._blocked:
            raise PermissionError(f"Image '{image}' is blocked.")

    def validate_container(
        self,
        container_id: str,
    ) -> None:

        if not container_id:
            raise PermissionError("Container id cannot be empty.")

    def is_privileged(self) -> bool:
        return self._privileged
