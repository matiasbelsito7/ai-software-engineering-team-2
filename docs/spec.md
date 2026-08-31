# Project Specification

## Overview

AI Software Engineering Team is a multi-agent platform that transforms natural language descriptions into production-ready applications. Users describe their app idea in plain language, and a team of 10 AI agents collaborates to generate the complete codebase.

## Target Audience

- Non-technical users who want to create software without coding knowledge
- Entrepreneurs validating app ideas quickly
- Portfolio demonstration of multi-agent AI systems

## Core Value Proposition

**"Describe your app, get your code."**

No technical knowledge required. The system handles architecture, backend, frontend, testing, and deployment configuration automatically.

---

## User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| `user` | Regular user who creates apps | Create projects (max 3 on Free tier), download code (paid tiers), manage account |
| `admin` | Platform administrator | View all users, view metrics, manage tiers, monitor projects |

---

## Tier System

### Free Tier — "Empieza Gratis"

| Parameter | Value |
|-----------|-------|
| Price | $0/month |
| Token budget | 50,000 tokens per project |
| Max iterations | 2 refinement loops |
| Max projects | 3 |
| App retention | 1 month, then deleted |
| Code download | Not available |
| Support | Community only |

### Starter Tier — "App Personal"

| Parameter | Value |
|-----------|-------|
| Price | $9.99/month |
| Token budget | 200,000 tokens per project |
| Max iterations | 5 refinement loops |
| Max projects | 10 |
| App retention | 6 months |
| Code download | Available as ZIP |
| Support | Email (48h response) |

### Pro Tier — "App Profesional"

| Parameter | Value |
|-----------|-------|
| Price | $29.99/month |
| Token budget | 1,000,000 tokens per project |
| Max iterations | 15 refinement loops |
| Max projects | 50 |
| App retention | 12 months |
| Code download | Available as ZIP |
| Support | Priority email (24h response) |

### Business Tier — "App de Negocio"

| Parameter | Value |
|-----------|-------|
| Price | $79.99/month |
| Token budget | 3,000,000 tokens per project |
| Max iterations | 30 refinement loops |
| Max projects | Unlimited |
| App retention | 24 months |
| Code download | Available as ZIP |
| Support | Dedicated support |

---

## Authentication System

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | None | Create new user account |
| POST | `/api/v1/auth/login` | None | Authenticate and get JWT |
| POST | `/api/v1/auth/refresh` | Refresh token | Get new access token |
| GET | `/api/v1/auth/me` | Bearer token | Get current user profile |
| PUT | `/api/v1/auth/me` | Bearer token | Update profile |
| POST | `/api/v1/auth/forgot-password` | None | Send password reset email |
| POST | `/api/v1/auth/reset-password` | Reset token | Set new password |

### JWT Configuration

- Access token expiration: 30 minutes
- Refresh token expiration: 7 days
- Algorithm: HS256
- Token storage: HTTP-only cookies (frontend) or Authorization header (API)

### Password Requirements

- Minimum 8 characters
- At least 1 uppercase, 1 lowercase, 1 number
- Hashed with bcrypt (12 rounds)

---

## Admin Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/admin/stats` | Admin token | Platform metrics |
| GET | `/api/v1/admin/users` | Admin token | List all users (paginated) |
| GET | `/api/v1/admin/users/{id}` | Admin token | Get user details |
| PUT | `/api/v1/admin/users/{id}` | Admin token | Update user (role, tier) |
| DELETE | `/api/v1/admin/users/{id}` | Admin token | Deactivate user |
| GET | `/api/v1/admin/projects` | Admin token | List all projects |
| GET | `/api/v1/admin/projects/{id}` | Admin token | Get project details |

### Admin Metrics Response

```json
{
  "total_users": 150,
  "active_users": 89,
  "total_projects": 320,
  "tokens_used_total": 12500000,
  "revenue_by_tier": {
    "free": 0,
    "starter": 450.00,
    "pro": 899.70,
    "business": 319.96
  },
  "projects_by_status": {
    "completed": 280,
    "running": 15,
    "failed": 25
  }
}
```

---

## Project Lifecycle

### 1. Creation

User describes app in natural language via wizard:

```
Paso 1: "Describe tu app"
  Ejemplo: "Quiero una app de tareas con login, donde los usuarios 
           puedan crear, editar y eliminar tareas. Que tenga un 
           dashboard con estadísticas."

Paso 2: "Elige tu plan"
  [Gratis] [Personal $9.99] [Profesional $29.99]

Paso 3: Confirmar y generar
  "Tu app tomará ~3 minutos en generarse y usará ~180K tokens"
```

### 2. Generation

The system executes the agent workflow:

```
Spec Agent → Planner → Architect → Backend → Frontend → Reviewer → QA → Documentation → DevOps → Git
```

Progress is displayed in real-time:

```
Analizando tu idea...          (Spec Agent)
Diseñando la arquitectura...   (Planner + Architect)
Construyendo el backend...     (Backend)
Construyendo el frontend...    (Frontend)
Revisando la calidad...        (Reviewer + QA)
Generando documentación...     (Documentation)
Preparando deploy...           (DevOps)
Empaquetando...                (Git)
```

### 3. Preview

User sees the generated app UI in an iframe. No code is shown.

### 4. Download

- Free tier: "Actualiza tu plan para descargar el código"
- Paid tiers: ZIP file with complete project

### 5. Retention

- Free: 1 month
- Starter: 6 months
- Pro: 12 months
- Business: 24 months

After retention period, project and files are deleted.

---

## Budget Enforcement

### Flow

```
User creates project with tier Starter (200K tokens)
  │
  ├─ Spec Agent executes    → gasta 10K  → budget restante: 190K
  ├─ Planner executes       → gasta 15K  → budget restante: 175K
  ├─ Architect executes     → gasta 12K  → budget restante: 163K
  ├─ Backend executes       → gasta 40K  → budget restante: 123K
  ├─ Frontend executes      → gasta 35K  → budget restante: 88K
  ├─ Reviewer detects issues → envía a Backend
  ├─ Backend re-executes    → gasta 30K  → budget restante: 58K
  ├─ Reviewer approves      → QA executes → gasta 20K → budget restante: 38K
  ├─ Documentation executes → gasta 10K  → budget restante: 28K
  ├─ DevOps executes        → gasta 8K   → budget restante: 20K
  └─ Git executes           → gasta 5K   → budget restante: 15K
  
  Resultado: 185K/200K tokens usados → App completa
```

### Budget Exhaustion

When budget is exhausted:
1. Current agent finishes its current operation
2. Workflow stops gracefully
3. User sees: "Se agotó el presupuesto de tu plan. Actualiza para continuar."
4. Partial progress is saved

---

## App Output Structure

### Generated Project Structure

```
generated-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── database/
│   ├── migrations/
│   └── seed.sql
├── docker-compose.yml
├── README.md
└── .env.example
```

### ZIP Contents

The downloaded ZIP includes:
- Complete source code
- README with setup instructions
- Docker Compose for local development
- Environment variable template
- Database migrations

---

## Technical Architecture

### System Layers

```
┌─────────────────────────────────────────────────┐
│              Frontend (React)                    │
│  Login | Register | Wizard | Preview | Admin    │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│              API Layer (FastAPI)                  │
│  Auth | Tasks | Projects | Admin | CostTracking  │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│           Orchestration (LangGraph)              │
│  Spec → Planner → Architect → Backend →          │
│  Frontend → Reviewer → QA → Doc → DevOps → Git   │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│            Agent Layer (10 agents)               │
│  BaseAgent lifecycle: validate → prepare → run   │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│         Infrastructure Layer                    │
│  LLM | RAG | Memory | Tools | Observability     │
└─────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12+ |
| API | FastAPI + Uvicorn |
| Orchestration | LangGraph + LangChain Core |
| LLM | OpenRouter (SSE streaming), Ollama |
| Frontend | React 19, TypeScript 6, Vite 8, Tailwind CSS 4 |
| Database | PostgreSQL (SQLAlchemy 2 + Alembic) |
| Cache | Redis 7 |
| Vector Store | Qdrant |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Observability | OpenTelemetry, structlog |
| Container | Docker + Docker Compose |

---

## Constraints

1. **Budget**: Maximum $5 LLM spend per project generation (portfolio project)
2. **Retention**: Projects auto-deleted after tier-specific period
3. **Free tier limits**: 3 projects max, 50K tokens, 2 iterations
4. **No payment processing**: Tiers are configured but no Stripe integration (portfolio)
5. **Admin-only metrics**: Admin cannot view generated code, only usage data
