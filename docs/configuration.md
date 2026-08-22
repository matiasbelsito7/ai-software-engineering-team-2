# Configuration

All configuration is loaded from environment variables. Create a `.env` file in the project root or set variables directly.

## App Settings

Prefix: `APP_`

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `AI Software Engineering Team` | Application name |
| `APP_VERSION` | `0.1.0` | Application version |
| `APP_ENVIRONMENT` | `development` | Environment (`development`, `testing`, `staging`, `production`) |
| `APP_DEBUG` | `false` | Enable debug mode |
| `APP_HOST` | `0.0.0.0` | Server host |
| `APP_PORT` | `8000` | Server port |
| `APP_RELOAD` | `false` | Enable auto-reload (dev only) |
| `APP_WORKERS` | `1` | Number of uvicorn workers |
| `APP_API_PREFIX` | `/api/v1` | REST API prefix |
| `APP_ALLOWED_ORIGINS` | `["*"]` | CORS allowed origins |
| `APP_ALLOWED_METHODS` | `["*"]` | CORS allowed methods |
| `APP_ALLOWED_HEADERS` | `["*"]` | CORS allowed headers |
| `APP_ALLOW_CREDENTIALS` | `true` | CORS allow credentials |

## LLM Settings

Prefix: `LLM_`

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `ollama` | Provider (`openrouter` or `ollama`) |
| `LLM_DEFAULT_MODEL` | — | Default model name |
| `LLM_TEMPERATURE` | `0.7` | Generation temperature |
| `LLM_MAX_TOKENS` | `4096` | Max tokens per generation |
| `LLM_TOP_P` | `1.0` | Top-p sampling |
| `LLM_STREAMING` | `true` | Enable streaming responses |
| `LLM_TRACK_COSTS` | `true` | Track token costs |

### OpenRouter

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_OPENROUTER_API_KEY` | — | OpenRouter API key (required) |
| `LLM_OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` | API base URL |

### Ollama

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `LLM_OLLAMA_DEFAULT_MODEL` | `llama3.1` | Default Ollama model |

## Database Settings

Prefix: `DATABASE_`

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_HOST` | `localhost` | PostgreSQL host |
| `DATABASE_PORT` | `5432` | PostgreSQL port |
| `DATABASE_NAME` | `ai_team` | Database name |
| `DATABASE_USERNAME` | `postgres` | Database user |
| `DATABASE_PASSWORD` | `postgres` | Database password |
| `DATABASE_POOL_SIZE` | `5` | Connection pool size |
| `DATABASE_MAX_OVERFLOW` | `10` | Max overflow connections |

## Redis Settings

Prefix: `REDIS_`

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_PASSWORD` | — | Redis password (optional) |
| `REDIS_DB` | `0` | Redis database number |
| `REDIS_POOL_SIZE` | `10` | Connection pool size |
| `REDIS_CACHE_TTL` | `3600` | Default cache TTL (seconds) |
| `REDIS_KEY_PREFIX` | `ai_team:` | Redis key prefix |

## Qdrant Settings

Prefix: `QDRANT_`

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_HOST` | `localhost` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant HTTP port |
| `QDRANT_GRPC_PORT` | `6334` | Qdrant gRPC port |
| `QDRANT_COLLECTION` | `ai_team` | Collection name |
| `QDRANT_VECTOR_SIZE` | `1536` | Embedding vector size |
| `QDRANT_DISTANCE` | `Cosine` | Distance metric |

## Docker Settings

Prefix: `DOCKER_`

| Variable | Default | Description |
|----------|---------|-------------|
| `DOCKER_HOST` | `unix:///var/run/docker.sock` | Docker daemon socket |
| `DOCKER_TLS` | `false` | Enable TLS |
| `DOCKER_TIMEOUT` | `60` | API call timeout (seconds) |
| `DOCKER_BLOCKED_IMAGES` | `["docker:dind", "docker:latest"]` | Blocked images |
| `DOCKER_MAX_CONTAINERS` | `50` | Max concurrent containers |
| `DOCKER_PRIVILEGED` | `false` | Allow privileged containers |

## HTTP Settings

Prefix: `HTTP_`

| Variable | Default | Description |
|----------|---------|-------------|
| `HTTP_CONNECT_TIMEOUT` | `10` | Connection timeout (seconds) |
| `HTTP_READ_TIMEOUT` | `30` | Read timeout (seconds) |
| `HTTP_WRITE_TIMEOUT` | `10` | Write timeout (seconds) |
| `HTTP_POOL_TIMEOUT` | `10` | Pool timeout (seconds) |

## Telemetry Settings

Prefix: `TELEMETRY_`

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEMETRY_LOGGING_ENABLED` | `true` | Enable structured logging |
| `TELEMETRY_LOG_LEVEL` | `INFO` | Log level |
| `TELEMETRY_TRACING_ENABLED` | `false` | Enable OpenTelemetry tracing |
| `TELEMETRY_TRACING_ENDPOINT` | — | OTLP endpoint URL |
| `TELEMETRY_METRICS_ENABLED` | `false` | Enable Prometheus metrics |
| `TELEMETRY_METRICS_PORT` | `9090` | Metrics server port |

## Environment File

```bash
# .env example

# LLM
LLM__PROVIDER=ollama
LLM__OLLAMA__BASE_URL=http://localhost:11434

# App
APP__ENVIRONMENT=development
APP__DEBUG=true
APP__PORT=8000

# Redis
REDIS__HOST=localhost
REDIS__PORT=6379

# Qdrant
QDRANT__HOST=localhost
QDRANT__PORT=6333
```

Note: Use `__` (double underscore) as the separator for nested settings in environment variables.
