"""
Enums shared by the DevOps agent.
"""

from __future__ import annotations

from enum import StrEnum


# ============================================================================
# Deployment Targets
# ============================================================================


class DeploymentTarget(StrEnum):
    """
    Target platform for a deployment artifact.
    """

    LOCAL = "local"

    DOCKER = "docker"

    DOCKER_COMPOSE = "docker_compose"

    KUBERNETES = "kubernetes"

    TERRAFORM = "terraform"

    GITHUB_ACTIONS = "github_actions"

    AWS = "aws"

    AZURE = "azure"

    GCP = "gcp"


# ============================================================================
# Deployment Environment
# ============================================================================


class DeploymentEnvironment(StrEnum):
    """
    Deployment environment.
    """

    DEVELOPMENT = "development"

    STAGING = "staging"

    PRODUCTION = "production"


# ============================================================================
# Infrastructure Type
# ============================================================================


class InfrastructureType(StrEnum):
    """
    Infrastructure artifact category.
    """

    CONTAINER = "container"

    ORCHESTRATION = "orchestration"

    CI_CD = "ci_cd"

    INFRASTRUCTURE = "infrastructure"

    CONFIGURATION = "configuration"

    MONITORING = "monitoring"

    NETWORK = "network"