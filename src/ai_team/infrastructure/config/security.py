"""
Security configuration.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    """
    Security-related application settings.
    """

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # API Key Authentication
    ###########################################################################

    auth_enabled: bool = Field(
        default=False,
        description="Enable API key authentication.",
    )

    api_keys: list[str] = Field(
        default_factory=list,
        description="Valid API keys. Requests must include one via X-API-Key header.",
    )

    auth_header: str = Field(
        default="X-API-Key",
        description="Header name for API key transmission.",
    )

    ###########################################################################
    # Rate Limiting
    ###########################################################################

    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable rate limiting.",
    )

    rate_limit_per_ip: int = Field(
        default=100,
        ge=1,
        description="Max requests per minute per IP address.",
    )

    rate_limit_per_key: int = Field(
        default=200,
        ge=1,
        description="Max requests per minute per API key.",
    )

    rate_limit_burst: int = Field(
        default=20,
        ge=1,
        description="Burst capacity for token bucket.",
    )

    ###########################################################################
    # Security Headers
    ###########################################################################

    security_headers_enabled: bool = Field(
        default=True,
        description="Add security headers to responses.",
    )

    hsts_max_age: int = Field(
        default=31536000,
        description="HSTS max-age in seconds (1 year default).",
    )

    content_security_policy: str = Field(
        default="default-src 'none'",
        description="Content-Security-Policy header value.",
    )

    ###########################################################################
    # Request Limits
    ###########################################################################

    max_request_body_size: int = Field(
        default=10 * 1024 * 1024,
        description="Max request body size in bytes (10MB default).",
    )

    ###########################################################################
    # JWT Authentication
    ###########################################################################

    jwt_secret: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
        description="Secret key for JWT signing.",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm.",
    )

    jwt_access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        description="Access token expiration in minutes.",
    )

    jwt_refresh_token_expire_days: int = Field(
        default=7,
        ge=1,
        description="Refresh token expiration in days.",
    )

    ###########################################################################
    # Audit Logging
    ###########################################################################

    audit_log_enabled: bool = Field(
        default=True,
        description="Enable security audit logging.",
    )

    audit_log_auth_attempts: bool = Field(
        default=True,
        description="Log authentication attempts.",
    )

    audit_log_rate_limits: bool = Field(
        default=True,
        description="Log rate limit violations.",
    )
