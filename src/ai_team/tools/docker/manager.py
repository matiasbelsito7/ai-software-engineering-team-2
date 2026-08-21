"""
Docker manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from docker import DockerClient  # type: ignore[attr-defined]


class DockerManager:
    """
    Wrapper around the Docker SDK.
    """

    def __init__(
        self,
        *,
        client: DockerClient,
    ) -> None:

        self._client = client

    # ------------------------------------------------------------------
    # Containers
    # ------------------------------------------------------------------

    def list_containers(
        self,
        *,
        all: bool = False,
    ) -> list[dict[str, Any]]:

        containers = self._client.containers.list(
            all=all,
        )

        return [
            {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": (container.image.tags[0] if container.image.tags else "<none>"),
            }
            for container in containers
        ]

    def start_container(
        self,
        container_id: str,
    ) -> None:

        self._client.containers.get(
            container_id,
        ).start()

    def stop_container(
        self,
        container_id: str,
    ) -> None:

        self._client.containers.get(
            container_id,
        ).stop()

    def remove_container(
        self,
        container_id: str,
        *,
        force: bool = False,
    ) -> None:

        self._client.containers.get(
            container_id,
        ).remove(
            force=force,
        )

    def run_container(
        self,
        *,
        image: str,
        command: str | None = None,
        detach: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:

        container = self._client.containers.run(
            image=image,
            command=command,
            detach=detach,
            **kwargs,
        )

        return {
            "id": container.id,
            "name": container.name,
        }

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    def list_images(
        self,
    ) -> list[dict[str, Any]]:

        images = self._client.images.list()

        return [
            {
                "id": image.id,
                "tags": image.tags,
            }
            for image in images
        ]

    def pull_image(
        self,
        image: str,
    ) -> None:

        self._client.images.pull(
            image,
        )

    def remove_image(
        self,
        image: str,
    ) -> None:

        self._client.images.remove(
            image,
        )

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def ping(
        self,
    ) -> bool:

        from docker.errors import DockerException

        try:
            return bool(
                self._client.ping(),
            )
        except DockerException:
            return False
