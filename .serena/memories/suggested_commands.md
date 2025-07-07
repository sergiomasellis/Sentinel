# Suggested Development Commands

## Essential Backend Commands
```bash
# Install dependencies
make install          # or: uv sync --dev

# Run development server
make dev             # or: uv run python run_dev.py

# Run tests
make test            # or: uv run pytest

# Lint code (MUST run before committing)
make lint            # or: uv run ruff check src/ tests/ && uv run mypy src/

# Format code
make format          # or: uv run black src/ tests/ && uv run isort src/ tests/
```

## Essential Frontend Commands
```bash
# Install dependencies
make frontend-install    # or: cd frontend && npm install

# Run development server
make frontend-dev        # or: cd frontend && npm run dev

# Build for production
make frontend-build      # or: cd frontend && npm run build
```

## Infrastructure Commands
```bash
# Start services (Redis, PostgreSQL)
make docker-up          # or: docker-compose up -d

# Stop services
make docker-down        # or: docker-compose down

# View logs
docker-compose logs -f [service-name]
```

## Development Workflow
```bash
# Before starting work
make docker-up       # Start dependencies
make dev            # Start backend (http://localhost:8000)
make frontend-dev   # Start frontend (http://localhost:5173)

# Before committing
make format         # Format code
make lint          # Check code quality
make test          # Run tests

# Install pre-commit hooks (one-time)
uv run pre-commit install
```

## System Commands (Linux)
- `git` - Version control
- `ls` - List files (aliased with color)
- `cd` - Change directory
- `rg` - ripgrep for fast searching (preferred over grep)
- `fd` - Modern find alternative
- `grep` - Text search (aliased with color and exclusions)