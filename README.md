# AI Software Engineering Team

Production-ready multi-agent AI software engineering platform built with LangGraph.

A team of 9 specialized AI agents that collaborate to plan, design, build, review, test, document, and deploy software projects through a structured workflow.

## Architecture

```
Planner → Architect → Backend → Frontend → Reviewer → QA → Documentation → DevOps → Git
    ↑                         ↑                                    │
    │                         └────────────────────────────────────┘
    │                                    (review loop)
    └─────────────────────────────────────────────────────────────────────
```

Each agent is powered by an LLM and has access to specialized tools (filesystem, terminal, git, code analysis, Docker, RAG, memory). The workflow is orchestrated via LangGraph with conditional routing — the Reviewer can send tasks back to Backend for revisions, and QA can trigger rework if tests fail.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- Docker & Docker Compose (optional, for containerized deployment)

### Installation

```bash
git clone https://github.com/matiasbelsito7/ai-software-engineering-team-2.git
cd ai-software-engineering-team-2
make install
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your settings (LLM provider API keys, etc.)
```

### Run Locally

```bash
make run
# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

### Run with Docker

```bash
make docker-build
make docker-up
# API available at http://localhost:8000
```

## API

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/tasks` | Submit a task (runs in background) |
| `GET` | `/api/v1/tasks` | List tasks with pagination |
| `GET` | `/api/v1/tasks/{id}` | Get task status and results |
| `DELETE` | `/api/v1/tasks/{id}` | Delete a task |
| `WS` | `/ws/tasks/{id}` | Real-time task progress |

### Example

```bash
# Submit a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a REST API for user management with CRUD operations"}'

# Check status
curl http://localhost:8000/api/v1/tasks/{task_id}
```

### WebSocket

Connect to `ws://localhost:8000/ws/tasks/{task_id}` for real-time progress:

```json
{"type": "progress", "task_id": "...", "status": "running", "agent": "backend", "progress": 0.4}
{"type": "complete", "task_id": "...", "status": "completed", "results": [...]}
```

## Project Structure

```
src/ai_team/
├── agents/          # 9 specialized AI agents
│   ├── planner/     # Task decomposition
│   ├── architect/   # System design
│   ├── backend/     # Backend implementation
│   ├── frontend/    # Frontend implementation
│   ├── reviewer/    # Code review
│   ├── qa/          # Quality assurance
│   ├── documentation/ # Documentation generation
│   ├── devops/      # Deployment & infrastructure
│   └── git/         # Version control
├── app/api/         # FastAPI application
│   ├── routers/     # API endpoints
│   ├── schemas/     # Request/response models
│   ├── middleware/   # Logging, error handling
│   └── exceptions/  # Custom error types
├── graph/           # LangGraph workflow orchestration
├── tools/           # 25+ tools (filesystem, git, Docker, RAG, etc.)
├── rag/             # Retrieval-Augmented Generation
├── memory/          # Agent memory (short-term, project, semantic)
├── context/         # Context management (selection, compression, summarization)
├── observability/   # Tracing, metrics, logging, cost tracking
├── evals/           # Evaluation framework with 5 heuristic metrics
└── infrastructure/  # Config, container, LLM providers, workspace
```

## Available Commands

```bash
make help           # Show all commands
make install        # Install dependencies
make run            # Start API server
make test           # Run all tests
make test-unit      # Run unit tests only
make lint           # Run linter
make typecheck      # Run type checker
make format         # Format code
make check          # Run all quality checks
make docker-up      # Start Docker services
make docker-down    # Stop Docker services
```

## Development

### Code Quality

- **Linting**: Ruff (configured in `pyproject.toml`)
- **Formatting**: Black
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with coverage

```bash
make check   # Runs format-check + lint + typecheck + test
```

### Architecture

The project follows a layered architecture:

- **Agents** → depend on tools, memory, RAG, context, observability
- **Tools** → depend on infrastructure (workspace, Docker, HTTP)
- **Graph** → orchestrates agents via LangGraph
- **API** → exposes agents via FastAPI
- **Infrastructure** → config, container, LLM providers

Run architecture validation:

```bash
make validate
```

## Tech Stack

- **Orchestration**: LangGraph, LangChain
- **LLM Providers**: OpenRouter, Ollama (OpenAI-compatible)
- **API**: FastAPI, uvicorn
- **Vector Store**: Qdrant (in-memory fallback)
- **Cache**: Redis
- **Observability**: OpenTelemetry, structlog
- **Evaluation**: Custom heuristic metrics
- **Containerization**: Docker, Docker Compose

## License

MIT License. See [LICENSE](LICENSE) for details.
