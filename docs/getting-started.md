# Getting Started

This guide walks you through setting up and running the AI Software Engineering Team.

## Prerequisites

- **Python 3.12+**
- **uv** — Fast Python package manager ([install](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker & Docker Compose** (optional, for containerized deployment)

## Installation

```bash
# Clone the repository
git clone https://github.com/matiasbelsito7/ai-software-engineering-team-2.git
cd ai-software-engineering-team-2

# Install all dependencies
make install

# Install pre-commit hooks (optional but recommended)
make install-hooks
```

## Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Key variables to configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM__PROVIDER` | `ollama` | LLM provider (`openrouter` or `ollama`) |
| `LLM__OPENROUTER__API_KEY` | — | OpenRouter API key (if using OpenRouter) |
| `LLM__OLLAMA__BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `APP__PORT` | `8000` | API server port |
| `APP__DEBUG` | `false` | Enable debug mode |

All configuration is loaded from environment variables with the appropriate prefix. See [Configuration Reference](configuration.md) for the full list.

## Running Locally

```bash
# Start the API server with hot reload
make run
```

The API is now available at:
- **API**: http://localhost:8000/api/v1
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running with Docker

```bash
# Build and start all services (app + Redis + Qdrant)
make docker-build
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

## Submitting Your First Task

```bash
# Submit a task via the API
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a REST API for user management with CRUD operations"}'
```

The response includes a `task_id` you can use to check progress:

```bash
# Check task status
curl http://localhost:8000/api/v1/tasks/{task_id}
```

Or connect via WebSocket for real-time updates:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/tasks/{task_id}");
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

## Development

### Code Quality

```bash
make format     # Format code with Black + Ruff
make lint       # Run Ruff linter
make typecheck  # Run mypy type checker
make test       # Run all tests
make check      # Run all quality checks at once
```

### Available Commands

```bash
make help       # Show all available commands
```

## Next Steps

- [Architecture Overview](architecture/overview.md) — Understand the system design
- [API Reference](api/reference.md) — Detailed API documentation
- [Configuration](configuration.md) — All configuration options
- [Deployment](deployment.md) — Production deployment guide
