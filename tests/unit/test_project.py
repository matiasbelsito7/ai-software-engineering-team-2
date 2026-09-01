"""
Tests for the project system.
"""

from __future__ import annotations

import pytest

from ai_team.domain.schemas.project import (
    CreateProjectRequest,
    ProjectStatsResponse,
    TierInfo,
    UpdateProjectRequest,
)

# ---------------------------------------------------------------------------
# Project schema tests
# ---------------------------------------------------------------------------


class TestProjectSchemas:
    """Test project Pydantic schemas."""

    def test_create_project_request(self):
        req = CreateProjectRequest(
            name="My App",
            description="A todo app",
            tier="free",
        )
        assert req.name == "My App"
        assert req.tier == "free"

    def test_create_project_request_defaults_to_free(self):
        req = CreateProjectRequest(
            name="App",
            description="Desc",
        )
        assert req.tier == "free"

    def test_create_project_request_empty_name_fails(self):
        with pytest.raises(ValueError):
            CreateProjectRequest(name="", description="Desc")

    def test_update_project_request(self):
        req = UpdateProjectRequest(name="New Name")
        assert req.name == "New Name"

    def test_tier_info(self):
        info = TierInfo(
            name="free",
            display_name="Empieza Gratis",
            price_monthly=0.0,
            tokens_per_project=50_000,
            max_iterations=2,
            max_projects=3,
            retention_days=30,
            can_download_code=False,
        )
        assert info.name == "free"
        assert info.can_download_code is False

    def test_project_stats_response(self):
        resp = ProjectStatsResponse(
            total_projects=5,
            projects_by_status={"completed": 3, "generating": 2},
            total_tokens_used=50_000,
            current_tier="free",
            projects_remaining=1,
        )
        assert resp.total_projects == 5
        assert resp.projects_remaining == 1
