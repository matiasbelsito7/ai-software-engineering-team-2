# Deployment Guide

## Docker Deployment (Recommended)

### Quick Start

```bash
# Build and start all services
make docker-build
make docker-up

# Verify
curl http://localhost:8000/api/v1/health
```

### Services

The `docker-compose.yml` starts three services:

| Service | Port | Description |
|---------|------|-------------|
| `app` | 8000 | AI Software Engineering Team API |
| `redis` | 6379 | Cache and session store |
| `qdrant` | 6333, 6334 | Vector database for RAG |

### Configuration

Environment variables are passed to the container via `docker-compose.yml`. Override them by creating a `.env` file or editing the compose file directly.

### Volumes

| Volume | Container Path | Purpose |
|--------|---------------|---------|
| `./workspace` | `/app/workspace` | Shared workspace for agent output |
| `redis-data` | `/data` | Redis persistence |
| `qdrant-data` | `/qdrant/storage` | Qdrant persistence |

### Production Build

```bash
# Build production image only
docker build --target production -t ai-team:latest .

# Run standalone
docker run -d \
  --name ai-team \
  -p 8000:8000 \
  -e LLM__PROVIDER=openrouter \
  -e LLM__OPENROUTER__API_KEY=your-key \
  ai-team:latest
```

### Health Checks

All services have built-in health checks:

```bash
# Check app health
curl http://localhost:8000/api/v1/health

# Check via Docker
docker compose ps
```

## Manual Deployment

### Requirements

- Python 3.12+
- Redis server
- Qdrant server (or use in-memory fallback)

### Steps

```bash
# Clone and install
git clone https://github.com/matiasbelsito7/ai-software-engineering-team-2.git
cd ai-software-engineering-team-2
make install

# Configure
cp .env.example .env
# Edit .env with your settings

# Run
make run
```

### Production Server

```bash
# With multiple workers
uvicorn ai_team.app.api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

## Environment Variables

See [Configuration Reference](configuration.md) for all available settings.

Critical variables for production:

```bash
# Required for OpenRouter
LLM__PROVIDER=openrouter
LLM__OPENROUTER__API_KEY=sk-or-...

# Security
APP__ALLOWED_ORIGINS=["https://yourdomain.com"]
APP__DEBUG=false
APP__ENVIRONMENT=production

# Redis (for production caching)
REDIS__HOST=redis
REDIS__PORT=6379
```

## Monitoring

### Health Endpoint

```
GET /api/v1/health
```

Returns application status, version, and uptime.

### Structured Logging

Logs are output in JSON format when `TELEMETRY__LOGGING_ENABLED=true`.

### OpenTelemetry

Enable distributed tracing:

```bash
TELEMETRY__TRACING_ENABLED=true
TELEMETRY__TRACING_ENDPOINT=http://jaeger:4318
```

## Troubleshooting

### Docker Build Fails

```bash
# Clean build
docker compose down
docker compose build --no-cache
```

### App Can't Connect to Redis

Ensure Redis is running and accessible:

```bash
docker compose ps redis
redis-cli -h localhost ping
```

### App Can't Connect to Qdrant

Ensure Qdrant is running and healthy:

```bash
docker compose ps qdrant
curl http://localhost:6333/healthz
```
