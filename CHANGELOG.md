# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-08-22

### Added

#### API for Frontend
- Request/response schemas for all endpoints (tasks, health, error)
- In-memory task store with CRUD operations
- POST `/tasks` returns 202 Accepted with task_id
- Task list pagination (offset/limit)
- Custom exception hierarchy (NotFound, Conflict, Validation, RateLimit, Internal)
- Error handlers with structured responses
- CORS middleware with configurable origins
- Request ID middleware for tracing
- `create_app()` factory for testability

#### Streaming and Feedback
- SSE streaming endpoint: `GET /tasks/{id}/stream`
- Stream events: task_start, agent_progress, task_complete, error, ping
- Feedback models (FeedbackRecord, FeedbackResponse, FeedbackType)
- FeedbackState with request/response flow
- BaseAgent.request_feedback() and get_feedback_response()
- Feedback API: `GET /tasks/{id}/feedback`, `POST /tasks/{id}/feedback/{id}`

#### Task Templates
- Template models (TaskTemplate, TemplateParameter, TemplateType)
- Template registry with register/get/list/search
- 6 built-in templates: REST API, CLI tool, documentation, refactoring, testing, database schema
- Template rendering with parameter substitution
- Template API: `GET /templates`, `GET /templates/{id}`, `POST /templates/{id}/render`, `POST /templates/{id}/create-task`

#### Security
- API key authentication middleware
- Rate limiting middleware (configurable per-endpoint)
- Security headers middleware (CSP, HSTS, X-Frame-Options)
- Request ID middleware for correlation
- Security audit logger
- SecuritySettings configuration

#### Docker
- Multi-stage Dockerfile (builder + runtime)
- Docker Compose with app, Redis, Qdrant
- .dockerignore for efficient builds
- DockerSettings configuration
- DockerTool, DockerManager, DockerPolicy

#### Documentation
- LICENSE file (MIT)
- README with architecture, quick start, API reference
- CONTRIBUTING guidelines with PR workflow
- CHANGELOG with all features
- .env.example with all configuration options
- docs/ directory with guides, architecture, API reference

#### Bug Fixes
- DatabaseAgent, DatabasePromptBuilder, RAGTool, MemoryTool wired to real managers
- Tool factory with proper dependency injection
- Container wiring for all tools and managers
- CORS middleware applied to all routes
- API prefix `/api/v1` applied to all routers

### Added (Items 1-10)

#### Item 4: Git Integration
- Extended `tools/git/commands.py` with 30+ git operations
- Branch management: create, delete, rename, merge, fetch, list remote
- Tag operations: create, list, delete
- Stash operations: push, pop, list, drop
- Remote operations: add, list, remove
- PR operations via `gh` CLI: create, list, view, checkout, merge, close
- Repository info: status, log, diff

#### Item 5: Automated Code Review
- `review/` package with ReviewEngine
- Pattern-based detection: security, performance, style, bugs
- Inline comments with severity (info/warning/error/critical)
- Review categories: bug, security, performance, style, docs, test, architecture
- Score calculation and approval logic
- API: `POST /review`

#### Item 6: Testing Pipeline
- `testing/` package with TestGenerator
- Support for pytest and unittest frameworks
- Source code analysis: extract functions, classes
- Test stub generation with assertions
- Coverage estimation and suggestions
- API: `POST /tests/generate`

#### Item 7: Deployment Automation
- `deployment/` package with PipelineGenerator
- GitHub Actions: ci.yml, deploy.yml workflows
- GitLab CI: .gitlab-ci.yml configuration
- Docker: Dockerfile, docker-compose.yml generation
- API: `POST /deployment/generate`

#### Item 8: Knowledge Base
- `knowledge/` package with KnowledgeStore
- Knowledge types: concept, procedure, reference, troubleshooting, best_practice, pattern, decision
- Full-text search with relevance scoring
- Tag and category indexes
- Search highlights extraction
- CRUD API: `POST/GET/DELETE /knowledge`, `GET /knowledge/search`, `GET /knowledge/stats`

#### Item 9: Multi-task Orchestration
- `orchestration/` package with OrchestrationEngine
- Topological sort for dependency resolution
- Pipeline stages with parallel task execution
- Task state tracking: pending, running, completed, failed, cancelled, blocked
- Runnable task detection based on dependency completion
- Priority-based task ordering
- API: `POST/GET/DELETE /orchestration/plans`, `GET execution-order`, `GET runnable`

#### Item 10: Cost Tracking
- `cost_tracking/` package with CostTracker
- Per-model pricing (OpenAI GPT-4o, GPT-4o-mini, GPT-3.5-turbo, Anthropic Claude 3)
- Cost recording: tokens, costs, provider, model, task/agent attribution
- Cost alerts with threshold and period (daily/weekly/monthly)
- Cost budgets with usage tracking and exceeded detection
- Cost summaries: by provider, model, agent, task
- API: `POST /cost-tracking/records`, `GET summary/stats`, `GET/POST/DELETE alerts`, `GET/POST/DELETE budgets`

## [0.1.0] - 2024-01-01

### Added

#### Core
- Multi-agent system with 9 specialized AI agents (Planner, Architect, Backend, Frontend, Reviewer, QA, Documentation, DevOps, Git)
- LangGraph-based workflow orchestration with conditional routing
- Agent execution lifecycle (prepare, validate, run, after_execution)
- RAG (Retrieval-Augmented Generation) with semantic and keyword retrieval
- Memory system (short-term, project, semantic stores)
- Context management (selection, compression, summarization)
- Evaluation framework with 5 heuristic metrics

#### Tools
- 25+ tools: Filesystem, Terminal, Git, Python, Search, Documentation, Repository
- Docker tool with container/image management
- HTTP and Browser tools
- Code analysis tools (formatter, analyzer, complexity, linter, type checker)
- Security scanner, test runner, dependency manager
- RAG and Memory tools wired to real managers

#### API
- FastAPI application with modular router structure
- Task CRUD: create (background), get, list, delete
- WebSocket endpoint for real-time task progress
- CORS middleware with configurable origins
- Request logging and error handling middleware
- Custom exception hierarchy

#### Infrastructure
- Dockerfile (multi-stage, production-ready)
- Docker Compose (app + Redis + Qdrant)
- Configuration system (App, LLM, Database, Redis, Qdrant, Docker, Telemetry, HTTP)
- Dependency injection container
- OpenTelemetry tracing and metrics
- Structured logging with structlog

#### DevOps
- GitHub Actions CI/CD (lint, test, coverage, security scanning)
- Makefile with 20+ commands
- Architecture validation script
- Pre-commit hooks

#### Documentation
- Project README with architecture overview
- Contributing guidelines
- API documentation (Swagger/ReDoc)
- Configuration reference
- Deployment guide
