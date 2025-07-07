# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Sentinel** is an AI-driven testing platform that automatically generates, executes, and self-heals tests based on code changes and requirements. The platform consists of:
- **Backend**: Python 3.12 + FastAPI orchestrator service
- **Frontend**: React + TypeScript + Tailwind CSS dashboard
- **AI Agent**: LangChain/LangGraph powered test generation using Azure OpenAI
- **Integrations**: Bitbucket, Jira, Harness CI, AWS ECS

## Technology Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Celery, Redis
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, shadcn/ui components
- **Database**: PostgreSQL with asyncpg
- **AI/ML**: LangChain, LangGraph, Azure OpenAI
- **Observability**: OpenTelemetry, Arize Phoenix, Structlog
- **Package Management**: uv (Python), npm (JavaScript)

## Development Commands

### Backend Development

```bash
# Install dependencies
make install
# or
uv sync --dev

# Run development server
make dev
# or
uv run python run_dev.py

# Run tests
make test
# or
uv run pytest

# Lint code
make lint
# or
uv run ruff check src/ tests/
uv run mypy src/

# Format code
make format
# or
uv run black src/ tests/
uv run isort src/ tests/
```

### Frontend Development

```bash
# Install frontend dependencies
make frontend-install
# or
cd frontend && npm install

# Run frontend dev server
make frontend-dev
# or
cd frontend && npm run dev

# Build frontend
make frontend-build
# or
cd frontend && npm run build
```

### Docker Services

```bash
# Start Redis and PostgreSQL
make docker-up
# or
docker-compose up -d

# Stop services
make docker-down
# or
docker-compose down
```

### Environment Setup

1. Copy `.env.example` to `.env` and configure:
   - Azure OpenAI credentials
   - Bitbucket and Jira API tokens
   - Database connection strings
   - Other service credentials

2. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Project Structure

```
Sentinel/
├── src/sentinel/          # Backend source code
│   ├── api/              # FastAPI endpoints
│   ├── agents/           # AI agents for test generation
│   ├── core/             # Core utilities (config, logging)
│   ├── integrations/     # External service clients
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── main.py          # FastAPI app entry point
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── lib/         # Utilities
│   │   └── App.tsx      # Main app component
│   └── package.json
├── tests/               # Test suite
├── docs/                # Documentation
├── pyproject.toml       # Python project config
├── docker-compose.yml   # Local services
└── Makefile            # Development shortcuts
```

## Architecture Overview

The platform follows an event-driven architecture:
1. **Webhook triggers** from CI/CD (Bitbucket/Harness) notify of code changes
2. **Test Orchestrator** fetches context (code diffs, Jira tickets)
3. **AI Agent** generates appropriate tests based on changes
4. **Test Runner** executes tests in parallel
5. **Self-Healing Agent** fixes failing tests automatically
6. **Results** are reported back to PR/Jira and monitoring systems

## Key Features to Implement

1. **Test Generation**:
   - E2E tests (Cypress) for UI changes
   - Integration tests (pytest) for API changes
   - Regression tests for bug fixes

2. **Self-Healing**:
   - Automatic test updates when selectors change
   - Intelligent failure analysis
   - Iterative fix attempts

3. **Observability**:
   - OpenTelemetry instrumentation
   - Arize Phoenix for LLM monitoring
   - Structured logging with Structlog

## API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/test-runs` - Create new test run
- `GET /api/v1/test-runs/{run_id}` - Get test run status
- `POST /api/v1/webhooks/bitbucket` - Bitbucket webhook
- `POST /api/v1/webhooks/harness` - Harness CI webhook

## Important Notes

- Always run linting before committing: `make lint`
- Use structured logging via `get_logger(__name__)`
- Follow the AI agent patterns in `src/sentinel/agents/`
- Frontend uses Tailwind utility classes for styling
- All async database operations use asyncpg