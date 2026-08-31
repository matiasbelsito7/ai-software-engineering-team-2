"""
Tier configuration for the monetization system.

Defines tier limits, pricing, and features.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TierConfig:
    """Configuration for a subscription tier."""

    name: str
    display_name: str
    price_monthly: float
    tokens_per_project: int
    max_iterations: int
    max_projects: int  # -1 = unlimited
    retention_days: int
    can_download_code: bool


# ---------------------------------------------------------------------------
# Tier definitions
# ---------------------------------------------------------------------------

TIERS: dict[str, TierConfig] = {
    "free": TierConfig(
        name="free",
        display_name="Empieza Gratis",
        price_monthly=0.0,
        tokens_per_project=50_000,
        max_iterations=2,
        max_projects=3,
        retention_days=30,
        can_download_code=False,
    ),
    "starter": TierConfig(
        name="starter",
        display_name="App Personal",
        price_monthly=9.99,
        tokens_per_project=200_000,
        max_iterations=5,
        max_projects=10,
        retention_days=180,
        can_download_code=True,
    ),
    "pro": TierConfig(
        name="pro",
        display_name="App Profesional",
        price_monthly=29.99,
        tokens_per_project=1_000_000,
        max_iterations=15,
        max_projects=50,
        retention_days=365,
        can_download_code=True,
    ),
    "business": TierConfig(
        name="business",
        display_name="App de Negocio",
        price_monthly=79.99,
        tokens_per_project=3_000_000,
        max_iterations=30,
        max_projects=-1,
        retention_days=730,
        can_download_code=True,
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DEFAULT_TIER = "free"
ALL_TIER_NAMES = list(TIERS.keys())


def get_tier(name: str) -> TierConfig:
    """Get tier config by name. Raises ValueError if not found."""
    if name not in TIERS:
        msg = f"Invalid tier: {name}. Must be one of {ALL_TIER_NAMES}"
        raise ValueError(msg)
    return TIERS[name]


def get_tier_names() -> list[str]:
    """Return all available tier names."""
    return ALL_TIER_NAMES.copy()
