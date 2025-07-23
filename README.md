# Sentinel - AI-Driven Testing Platform

Sentinel is an AI-driven testing platform that automatically generates, executes, and self-heals tests based on code changes and requirements. It integrates with your CI/CD pipeline to provide continuous, intelligent test coverage.

## Features

- **AI-Powered Test Generation**: Automatically generates E2E, integration, and regression tests based on code changes
- **Self-Healing Tests**: Automatically fixes failing tests when selectors or assertions change
- **Multi-Source Context**: Pulls context from Bitbucket (code), Jira (requirements), and CI/CD pipelines
- **Parallel Execution**: Runs tests concurrently for faster feedback
- **Comprehensive Observability**: Built-in monitoring with OpenTelemetry and Arize Phoenix

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker and Docker Compose
- uv (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sergiomasellis/Sentinel.git
   cd Sentinel
   ```

2. Copy environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Install dependencies:
   ```bash
   make install
   make frontend-install
   ```

4. Start services:
   ```bash
   make docker-up
   ```

5. Run development servers:
   ```bash
   # Backend (in one terminal)
   make dev

   # Frontend (in another terminal)
   make frontend-dev
   ```

The backend will be available at http://localhost:8000 and the frontend at http://localhost:5173.

See the [Architecture](#architecture) section below for more details on how Sentinel works.

## Architecture

Sentinel follows an event-driven architecture:

1. **Webhook Triggers**: CI/CD systems notify Sentinel of code changes
2. **Context Gathering**: Fetches code diffs from Bitbucket and requirements from Jira
3. **AI Test Generation**: LangChain/LangGraph agent generates appropriate tests
4. **Parallel Execution**: Tests run concurrently in isolated containers
5. **Self-Healing**: AI agent analyzes failures and fixes tests automatically
6. **Reporting**: Results are posted back to PRs and Jira tickets

## Development

See [CLAUDE.md](./CLAUDE.md) for detailed development instructions and project structure.

### Running Tests

```bash
make test
```

### Linting and Formatting

```bash
make lint
make format
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
