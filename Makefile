```makefile
################################################################################
# AI Software Engineering Team
# Makefile
################################################################################

.DEFAULT_GOAL := help

################################################################################
# Variables
################################################################################

UV              := uv
PYTHON          := python3

SRC_DIR         := src
TEST_DIR        := tests

################################################################################
# Help
################################################################################

.PHONY: help

help: ## Show available commands
	@echo ""
	@echo "AI Software Engineering Team"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

################################################################################
# Environment
################################################################################

.PHONY: install

install: ## Install project dependencies
	$(UV) sync

.PHONY: update

update: ## Upgrade dependencies
	$(UV) lock --upgrade
	$(UV) sync

.PHONY: lock

lock: ## Update uv.lock
	$(UV) lock

################################################################################
# Cleaning
################################################################################

.PHONY: clean

clean: ## Remove caches and build artifacts
	$(UV) run python scripts/clean.py

################################################################################
# Formatting
################################################################################

.PHONY: format

format: ## Format source code
	$(UV) run black $(SRC_DIR) $(TEST_DIR)
	$(UV) run ruff check --fix $(SRC_DIR) $(TEST_DIR)

.PHONY: format-check

format-check: ## Check formatting
	$(UV) run black --check $(SRC_DIR) $(TEST_DIR)

################################################################################
# Linting
################################################################################

.PHONY: lint

lint: ## Run Ruff
	$(UV) run ruff check $(SRC_DIR) $(TEST_DIR)

################################################################################
# Type Checking
################################################################################

.PHONY: typecheck

typecheck: ## Run MyPy
	$(UV) run mypy

################################################################################
# Tests
################################################################################

.PHONY: test

test: ## Run all tests
	$(UV) run pytest

.PHONY: test-unit

test-unit: ## Run unit tests
	$(UV) run pytest -m unit

.PHONY: test-integration

test-integration: ## Run integration tests
	$(UV) run pytest -m integration

.PHONY: test-e2e

test-e2e: ## Run end-to-end tests
	$(UV) run pytest -m e2e

.PHONY: coverage

coverage: ## Generate coverage report
	$(UV) run pytest --cov

################################################################################
# Evaluation
################################################################################

.PHONY: evals

evals: ## Run AI evaluation suite
	$(UV) run python -m ai_team.evals.runner

################################################################################
# Architecture
################################################################################

.PHONY: validate

validate: ## Validate project architecture
	$(UV) run python scripts/validate_architecture.py

################################################################################
# Quality
################################################################################

.PHONY: check

check: format-check lint typecheck test ## Run complete quality validation

################################################################################
# Continuous Integration
################################################################################

.PHONY: ci

ci: clean check validate ## Run the complete CI pipeline locally

################################################################################
# Git Hooks
################################################################################

.PHONY: install-hooks

install-hooks: ## Install pre-commit hooks
	$(UV) run pre-commit install

.PHONY: hooks

hooks: ## Run pre-commit hooks
	$(UV) run pre-commit run --all-files

################################################################################
# Docker
################################################################################

.PHONY: docker-build

docker-build: ## Build Docker images
	docker compose build

.PHONY: docker-up

docker-up: ## Start containers
	docker compose up -d

.PHONY: docker-down

docker-down: ## Stop containers
	docker compose down

.PHONY: docker-logs

docker-logs: ## Show container logs
	docker compose logs -f

################################################################################
# Release
################################################################################

.PHONY: release

release: ci ## Placeholder for release process
	@echo "Release workflow is managed by GitHub Actions."

################################################################################
# End
################################################################################
```
