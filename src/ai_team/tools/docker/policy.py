"""
Docker execution policy.
"""

from __future__ import annotations


class DockerPolicy:
    """
    Validate Docker operations.
    """

    BLOCKED_IMAGES = {
        "docker:dind",
    }

    def validate_operation(
        self,
        operation: str,
    ) -> None:

        if not operation:

            raise PermissionError(
                "Operation cannot be empty."
            )

    def validate_image(
        self,
        image: str,
    ) -> None:

        if not image:

            raise PermissionError(
                "Image cannot be empty."
            )

        if image in self.BLOCKED_IMAGES:

            raise PermissionError(
                f"Image '{image}' is blocked."
            )

    def validate_container(
        self,
        container_id: str,
    ) -> None:

        if not container_id:

            raise PermissionError(
                "Container id cannot be empty."
            )