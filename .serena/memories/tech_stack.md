# Technology Stack

## Backend (Python 3.12+)
- **Framework**: FastAPI v0.115.0+
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy v2.0.36+
- **Task Queue**: Celery v5.4.0+ with Redis
- **Package Manager**: uv (modern Python package manager)

## AI/ML Stack
- **LangChain**: v0.3.0+ for AI orchestration
- **LangGraph**: v0.2.0+ for agent workflows
- **Azure OpenAI**: via langchain-openai for LLM capabilities

## Frontend
- **Framework**: React v19.1.0 with TypeScript
- **Build Tool**: Vite v7.0.0
- **Styling**: Tailwind CSS v4.1.11 + shadcn/ui components
- **State Management**: Built-in React hooks
- **Icons**: Lucide React

## Infrastructure & DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: Pre-commit hooks, GitHub Actions ready
- **Observability**: 
  - OpenTelemetry for distributed tracing
  - Arize Phoenix v5.0.0+ for LLM monitoring
  - Structlog v24.4.0+ for structured logging

## External Integrations
- **Atlassian Python API**: Jira integration
- **Boto3**: AWS services integration
- **Bitbucket**: Code repository integration
- **Harness CI**: CI/CD platform integration