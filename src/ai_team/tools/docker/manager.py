"""
Docker manager.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from docker import DockerClient


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
        ports: dict[str, Any] | None = None,
        volumes: dict[str, Any] | None = None,
        environment: dict[str, str] | None = None,
        network: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:

        run_kwargs: dict[str, Any] = {
            "image": image,
            "command": command,
            "detach": detach,
        }

        if ports is not None:
            run_kwargs["ports"] = ports

        if volumes is not None:
            run_kwargs["volumes"] = volumes

        if environment is not None:
            run_kwargs["environment"] = environment

        if network is not None:
            run_kwargs["network"] = network

        if name is not None:
            run_kwargs["name"] = name

        run_kwargs.update(kwargs)

        container = self._client.containers.run(**run_kwargs)

        return {
            "id": container.id,
            "name": container.name,
        }

    def get_container_logs(
        self,
        container_id: str,
        *,
        tail: int = 100,
        since: str | None = None,
    ) -> str:

        container = self._client.containers.get(container_id)

        raw: bytes = container.logs(
            tail=tail,
            since=since,
        )

        return raw.decode("utf-8", errors="replace")

    def exec_in_container(
        self,
        container_id: str,
        *,
        command: str,
        workdir: str | None = None,
        user: str | None = None,
    ) -> dict[str, Any]:

        container = self._client.containers.get(container_id)

        exit_code, output = container.exec_run(
            cmd=command,
            workdir=workdir,
            user=user,
            demux=True,
        )

        stdout = output[0].decode("utf-8", errors="replace") if output[0] else ""
        stderr = output[1].decode("utf-8", errors="replace") if output[1] else ""

        return {
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
        }

    def inspect_container(
        self,
        container_id: str,
    ) -> dict[str, Any]:

        container = self._client.containers.get(container_id)

        return container.attrs  # type: ignore[no-any-return]

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

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the Docker client connection."""

        self._client.close()
