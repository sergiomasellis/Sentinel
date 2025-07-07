# Project Structure

## Root Directory
```
Sentinel/
├── src/sentinel/          # Backend Python package
├── frontend/              # React TypeScript frontend
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .serena/              # Serena AI assistant data
├── .claude/              # Claude assistant data
├── pyproject.toml        # Python project configuration
├── Makefile              # Development shortcuts
├── docker-compose.yml    # Local services (Redis, PostgreSQL)
├── Dockerfile            # Container definition
├── CLAUDE.md            # AI assistant instructions
├── README.md            # Project documentation
├── .env.example         # Environment variables template
└── run_dev.py           # Development server runner
```

## Backend Structure (src/sentinel/)
```
src/sentinel/
├── __init__.py
├── main.py              # FastAPI application entry point
├── api/                 # REST API endpoints
│   ├── health.py       # Health check endpoints
│   ├── test_runs.py    # Test run management
│   └── webhooks.py     # Webhook handlers (Bitbucket, Harness)
├── agents/              # AI agents
│   └── test_generator.py # LangChain/LangGraph test generation
├── core/                # Core utilities
│   ├── config.py       # Configuration management
│   └── logging.py      # Structured logging setup
├── integrations/        # External service clients
│   ├── bitbucket.py    # Bitbucket API client
│   └── jira.py         # Jira API client
├── models/              # Database models
│   ├── base.py         # SQLAlchemy base classes
│   └── test_run.py     # Test run data models
├── services/            # Business logic layer
└── utils/               # Utility functions
```

## Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── lib/            # Utilities and helpers
│   ├── App.tsx         # Main application component
│   └── index.tsx       # Entry point
├── public/             # Static assets
├── package.json        # Dependencies
└── vite.config.ts      # Vite configuration
```

## Key Design Patterns
- **Layered Architecture**: Clear separation between API, services, and data layers
- **Dependency Injection**: Configuration and services injected via FastAPI
- **Async-First**: All I/O operations use async/await
- **Domain-Driven**: Models reflect business domain (test runs, results)