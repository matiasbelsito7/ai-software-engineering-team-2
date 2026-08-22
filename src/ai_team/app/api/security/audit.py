"""
Security audit logging.
"""

from __future__ import annotations

import logging
from enum import StrEnum


class SecurityEvent(StrEnum):
    """Security event types."""

    AUTH_SUCCESS = "AUTH_SUCCESS"
    AUTH_FAIL_MISSING = "AUTH_FAIL_MISSING"
    AUTH_FAIL_INVALID = "AUTH_FAIL_INVALID"
    RATE_LIMIT_IP = "RATE_LIMIT_IP"
    RATE_LIMIT_KEY = "RATE_LIMIT_KEY"
    SUSPICIOUS_INPUT = "SUSPICIOUS_INPUT"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"


class SecurityAuditLogger:
    """
    Structured security audit logger.

    Logs security-relevant events with consistent formatting
    for downstream analysis and alerting.
    """

    def __init__(
        self,
        *,
        logger_name: str = "ai_team.security.audit",
    ) -> None:
        self._logger = logging.getLogger(logger_name)

    def log_event(
        self,
        *,
        event: SecurityEvent,
        path: str,
        ip: str | None = None,
        api_key_suffix: str | None = None,
        detail: str | None = None,
        level: int = logging.INFO,
    ) -> None:
        parts = [
            f"event={event.value}",
            f"path={path}",
        ]

        if ip:
            parts.append(f"ip={ip}")

        if api_key_suffix:
            parts.append(f"key=***{api_key_suffix}")

        if detail:
            parts.append(f"detail={detail}")

        message = " ".join(parts)

        self._logger.log(level, message)

    def auth_success(
        self,
        *,
        path: str,
        ip: str | None = None,
        api_key_suffix: str | None = None,
    ) -> None:
        self.log_event(
            event=SecurityEvent.AUTH_SUCCESS,
            path=path,
            ip=ip,
            api_key_suffix=api_key_suffix,
        )

    def auth_fail_missing(
        self,
        *,
        path: str,
        ip: str | None = None,
    ) -> None:
        self.log_event(
            event=SecurityEvent.AUTH_FAIL_MISSING,
            path=path,
            ip=ip,
            level=logging.WARNING,
        )

    def auth_fail_invalid(
        self,
        *,
        path: str,
        ip: str | None = None,
        api_key_suffix: str | None = None,
    ) -> None:
        self.log_event(
            event=SecurityEvent.AUTH_FAIL_INVALID,
            path=path,
            ip=ip,
            api_key_suffix=api_key_suffix,
            level=logging.WARNING,
        )

    def rate_limit(
        self,
        *,
        path: str,
        ip: str | None = None,
        api_key_suffix: str | None = None,
        limit_type: str = "ip",
    ) -> None:
        event = SecurityEvent.RATE_LIMIT_KEY if limit_type == "key" else SecurityEvent.RATE_LIMIT_IP
        self.log_event(
            event=event,
            path=path,
            ip=ip,
            api_key_suffix=api_key_suffix,
            level=logging.WARNING,
        )

    def suspicious_input(
        self,
        *,
        path: str,
        ip: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.log_event(
            event=SecurityEvent.SUSPICIOUS_INPUT,
            path=path,
            ip=ip,
            detail=detail,
            level=logging.WARNING,
        )
