"""
Tests for the authentication system.
"""

from __future__ import annotations

import time
from unittest.mock import MagicMock

import pytest

from ai_team.domain.models.tier import TIERS, get_tier
from ai_team.domain.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


# ---------------------------------------------------------------------------
# Tier config tests
# ---------------------------------------------------------------------------


class TestTierConfig:
    """Test tier configuration."""

    def test_all_tiers_exist(self):
        assert set(TIERS.keys()) == {"free", "starter", "pro", "business"}

    def test_free_tier_defaults(self):
        tier = get_tier("free")
        assert tier.price_monthly == 0.0
        assert tier.max_projects == 3
        assert tier.can_download_code is False
        assert tier.tokens_per_project == 50_000

    def test_starter_tier_can_download(self):
        tier = get_tier("starter")
        assert tier.can_download_code is True
        assert tier.price_monthly == 9.99

    def test_pro_tier_limits(self):
        tier = get_tier("pro")
        assert tier.tokens_per_project == 1_000_000
        assert tier.max_iterations == 15
        assert tier.max_projects == 50

    def test_business_tier_unlimited_projects(self):
        tier = get_tier("business")
        assert tier.max_projects == -1  # unlimited
        assert tier.price_monthly == 79.99

    def test_get_invalid_tier_raises(self):
        with pytest.raises(ValueError, match="Invalid tier"):
            get_tier("nonexistent")


# ---------------------------------------------------------------------------
# Auth schema tests
# ---------------------------------------------------------------------------


class TestAuthSchemas:
    """Test auth Pydantic schemas."""

    def test_register_request_valid(self):
        req = RegisterRequest(email="test@example.com", password="StrongPass1")
        assert req.email == "test@example.com"
        assert req.password == "StrongPass1"

    def test_register_request_invalid_email(self):
        with pytest.raises(Exception):
            RegisterRequest(email="not-an-email", password="StrongPass1")

    def test_register_request_short_password(self):
        with pytest.raises(Exception):
            RegisterRequest(email="test@example.com", password="short")

    def test_login_request(self):
        req = LoginRequest(email="user@test.com", password="pass123")
        assert req.email == "user@test.com"

    def test_token_response(self):
        resp = TokenResponse(
            access_token="abc",
            refresh_token="xyz",
            token_type="bearer",
            expires_in=1800,
        )
        assert resp.access_token == "abc"
        assert resp.token_type == "bearer"
        assert resp.expires_in == 1800

    def test_token_response_fields(self):
        resp = TokenResponse(
            access_token="abc",
            refresh_token="xyz",
            token_type="bearer",
            expires_in=1800,
        )
        assert resp.access_token == "abc"
        assert resp.token_type == "bearer"
        assert resp.expires_in == 1800
