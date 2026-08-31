"""
App generator service.

Orchestrates the full generation pipeline:
  project creation → workflow execution → file output → preview → ZIP.
"""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Any

from ai_team.domain.models.tier import get_tier
from ai_team.domain.services.app_packager import AppPackager
from ai_team.domain.services.app_preview import AppPreview
from ai_team.domain.services.project_service import ProjectService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AppGenerationError(Exception):
    """Raised when app generation fails."""


class AppGenerator:
    """
    Orchestrates the full application generation pipeline.
    """

    def __init__(
        self,
        session: AsyncSession,
        graph: Any,
    ) -> None:
        self._session = session
        self._graph = graph
        self._project_service = ProjectService(session)

    async def generate(
        self,
        *,
        user_id: uuid.UUID,
        name: str,
        description: str,
        tier: str = "free",
    ) -> dict[str, Any]:
        """
        Generate an application from a natural language description.

        Args:
            user_id: ID of the user requesting generation.
            name: Project name.
            description: Natural language app description.
            tier: Tier slug (free, starter, pro, business).

        Returns:
            Dict with project_id, status, preview_html, and files_path.

        Raises:
            AppGenerationError: If generation fails.
            BudgetExhaustedError: If tier limits are exceeded.
        """

        tier_config = get_tier(tier)

        project = await self._project_service.create(
            user_id=user_id,
            name=name,
            description=description,
            tier=tier,
        )

        project_id = str(project.id)

        try:
            await self._project_service.update_status(
                project_id=project_id,
                user_id=user_id,
                status="generating",
            )

            final_state = await self._run_workflow(
                description=description,
                tier=tier,
                tokens_budget=tier_config.tokens_per_project,
                max_iterations=tier_config.max_iterations,
                project_id=project_id,
            )

            files = self._extract_files(final_state)
            tokens_used = final_state.budget.tokens_used

            await self._project_service.record_tokens(
                project_id=project_id,
                user_id=user_id,
                tokens=tokens_used,
            )

            preview_html = AppPreview.generate(
                files=files,
                app_name=name,
            )

            files_path = f"workspace/{project_id}"
            await self._save_files(files_path, files)

            await self._project_service.update_status(
                project_id=project_id,
                user_id=user_id,
                status="completed",
            )

            await self._project_service.update(
                project_id=project_id,
                user_id=user_id,
                files_path=files_path,
            )

            return {
                "project_id": project_id,
                "status": "completed",
                "tokens_used": tokens_used,
                "preview_html": preview_html,
                "files_path": files_path,
                "files_count": len(files),
            }

        except Exception as exc:
            logger.exception(
                "App generation failed for project %s",
                project_id,
            )

            try:
                await self._project_service.update_status(
                    project_id=project_id,
                    user_id=user_id,
                    status="failed",
                )
            except Exception:
                logger.exception("Failed to update project status to failed")

            raise AppGenerationError(
                f"Generation failed: {exc}",
            ) from exc

    async def generate_zip(
        self,
        *,
        project_id: str,
        user_id: uuid.UUID,
    ) -> bytes:
        """
        Generate a ZIP archive for a completed project.

        Args:
            project_id: ID of the project.
            user_id: ID of the owner.

        Returns:
            ZIP file contents as bytes.
        """

        project = await self._project_service.get(
            project_id=project_id,
            user_id=user_id,
        )

        if not project.files_path:
            raise AppGenerationError("Project has no generated files")

        files = await self._load_files(project.files_path)

        readme = AppPackager.build_readme(
            app_name=project.name,
            description=project.description,
        )

        return AppPackager.create_zip(
            files=files,
            readme_content=readme,
        )

    async def _run_workflow(
        self,
        *,
        description: str,
        tier: str,
        tokens_budget: int,
        max_iterations: int,
        project_id: str,
    ) -> Any:
        """
        Execute the LangGraph workflow.
        """

        from ai_team.graph.state import (
            BudgetState,
            ConversationState,
            ExecutionState,
            GraphState,
        )

        initial_state = GraphState(
            conversation=ConversationState(
                user_request=description,
            ),
            execution=ExecutionState(),
            budget=BudgetState(
                tier=tier,
                tokens_budget=tokens_budget,
                max_iterations=max_iterations,
                project_id=project_id,
            ),
        )

        final_state = await self._graph.ainvoke(initial_state)

        return final_state

    @staticmethod
    def _extract_files(state: Any) -> dict[str, str]:
        """
        Extract generated files from the final graph state.
        """

        files: dict[str, str] = {}

        if hasattr(state, "artifacts") and state.artifacts:
            files.update(state.artifacts.shared_files)

        if hasattr(state, "specification") and state.specification:
            spec = state.specification
            files["_specification.json"] = spec.model_dump_json(indent=2)

        return files

    @staticmethod
    async def _save_files(
        base_path: str,
        files: dict[str, str],
    ) -> None:
        """
        Save generated files to the filesystem.
        """

        from pathlib import Path

        root = Path(base_path)
        root.mkdir(parents=True, exist_ok=True)

        for rel_path, content in files.items():
            file_path = root / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

    @staticmethod
    async def _load_files(
        base_path: str,
    ) -> dict[str, str]:
        """
        Load files from a project directory.
        """

        from pathlib import Path

        root = Path(base_path)
        files: dict[str, str] = {}

        if not root.exists():
            return files

        for file_path in sorted(root.rglob("*")):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(root))
                files[rel_path] = file_path.read_text(encoding="utf-8")

        return files
