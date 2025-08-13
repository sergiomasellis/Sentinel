---
# Sentinel Implementation Outline

This document outlines the concrete steps to complete the core functionality for the Sentinel platform. Each step references existing files and specifies exact new files to create or modify.

## 0) Goals and Scope
- Persist and manage test runs
- Generate tests via the AI agent using repo diffs and Jira context
- Execute background tasks with Celery + Redis
- Add observability with OpenTelemetry
- Secure and process webhooks (Bitbucket, Harness)

Focus on the backend (FastAPI) and worker pieces. Frontend integration is noted but not required for this milestone.

Project version: 0.1.0

Repository references:
- FastAPI app: src/sentinel/main.py
- Config: src/sentinel/core/config.py
- Logging: src/sentinel/core/logging.py
- Models: src/sentinel/models/base.py, src/sentinel/models/test_run.py
- API: src/sentinel/api/health.py, src/sentinel/api/test_runs.py, src/sentinel/api/webhooks.py
- Agents: src/sentinel/agents/test_generator.py
- Integrations: src/sentinel/integrations/bitbucket.py, src/sentinel/integrations/jira.py
- Docker: docker-compose.yml, Dockerfile
- Env template: .env.example


## 1) Persistence Layer (Database and Migrations)

1.1 Create async SQLAlchemy engine/session
- New file: src/sentinel/core/db.py
- Contents (outline):
  - create_async_engine(settings.DATABASE_URL)
  - async_sessionmaker(bind=engine, expire_on_commit=False)
  - async dependency get_session() -> AsyncGenerator[AsyncSession, None]

1.2 Initialize DB in app lifespan
- Modify src/sentinel/main.py in lifespan() to test a DB connection on startup and log readiness.
- Add a shutdown hook if needed.

1.3 Alembic migrations
- Add Alembic to the project:
  - Create alembic.ini at repo root and alembic/ directory.
  - In alembic/env.py, set target_metadata = sentinel.models.base.Base.metadata
  - Generate initial migration to create test_runs table from src/sentinel/models/test_run.py
- Commands (for docs):
  - uv run alembic init alembic
  - Configure env.py, script_location
  - uv run alembic revision --autogenerate -m "init"
  - uv run alembic upgrade head


## 2) Test Run Service and API

2.1 Service layer
- New file: src/sentinel/services/test_runs.py
- Functions:
  - async create_test_run(session, request: TestRunRequest) -> TestRun
  - async get_test_run(session, run_id: UUID) -> TestRun | None
  - async list_test_runs(session, filters) -> List[TestRun]
  - async update_status(session, run_id: UUID, status: TestRunStatus, counts/results)

2.2 API wiring
- Modify src/sentinel/api/test_runs.py:
  - Use DB session dependency from src/sentinel/core/db.py
  - In POST /test-runs: persist record via service, enqueue Celery task (see Section 3), return real run_id and status
  - Implement GET /test-runs/{run_id}: return persisted status/result or 404
  - Add new endpoint: GET /test-runs to list with optional query params: status, branch, date range
- Keep Pydantic request/response models local or extract to src/sentinel/api/schemas.py if preferred.


## 3) Task Queue (Celery + Redis)

3.1 Celery app
- New file: src/sentinel/tasks/celery_app.py
- Configure Celery using Redis broker/backend from settings (see Section 6 for config additions).
- Name: "sentinel"

3.2 Test run tasks
- New file: src/sentinel/tasks/test_run_tasks.py
- Task: generate_and_execute_tests(run_id: str)
  - Flow:
    1) Set TestRun status to in_progress
    2) Resolve repo coordinates (workspace, repo_slug) from request.repository_url
    3) Fetch diff via src/sentinel/integrations/bitbucket.py -> BitbucketClient.get_commit_diff(...)
    4) If jira_ticket_id present, fetch context via src/sentinel/integrations/jira.py -> JiraClient.get_issue_details(...)
    5) Call AI agent src/sentinel/agents/test_generator.py -> TestGeneratorAgent.generate_tests(...)
    6) Optionally validate with validate_test_code(...)
    7) Persist results JSON, counts, and set status to completed
    8) On exceptions, set status to failed and record error_message

3.3 Docker Compose worker service
- Modify docker-compose.yml to add Celery worker:

  services:
    worker:
      build: .
      depends_on:
        - redis
        - postgres
      environment:
        - DATABASE_URL=postgresql+asyncpg://sentinel:sentinel@postgres:5432/sentinel
        - REDIS_URL=redis://redis:6379/0
      command: uv run celery -A sentinel.tasks.celery_app.celery_app worker --loglevel=INFO
      volumes:
        - .:/app

- Note: Consider a separate beat service later for periodic cleanups.


## 4) AI Agent Tooling Enhancements

4.1 Add tools to agent
- Modify src/sentinel/agents/test_generator.py in _setup_tools():
  - Tool: fetch_diff(workspace, repo_slug, commit_id) -> uses BitbucketClient.get_commit_diff
  - Tool: read_existing_tests(glob_pattern) -> reads files under tests/ and frontend (Cypress when added)
  - Tool: validate_python(code) -> lightweight syntax check (ast.parse) for pytest snippets

4.2 Use tools in prompts
- Ensure MessagesPlaceholder("agent_scratchpad") is correctly spelled and utilized
- Use create_openai_tools_agent to bind tools


## 5) Webhooks (Bitbucket, Harness)

5.1 Security and config
- Add shared secrets to settings (Section 6): BITBUCKET_WEBHOOK_SECRET, HARNESS_WEBHOOK_SECRET
- Validate signatures:
  - Bitbucket: HMAC-SHA256 of raw body with secret; compare to header (e.g., X-Hub-Signature or configured custom header)
  - Harness: validate X-Harness-Webhook-Token or HMAC if configured

5.2 Bitbucket handler
- Modify src/sentinel/api/webhooks.py -> bitbucket_webhook():
  - Verify signature
  - Parse x_event_key (e.g., repo:push, pullrequest:created/updated)
  - Extract repo URL/branch/commit
  - Create TestRun via service and enqueue task
  - Return 202

5.3 Harness handler
- Modify src/sentinel/api/webhooks.py -> harness_webhook():
  - Verify token/signature
  - Optionally correlate to an existing run and update status, or trigger execution


## 6) Configuration and Environment

6.1 Update settings
- Modify src/sentinel/core/config.py to add:
  - CELERY_BROKER_URL: Optional[str] = None  # default to REDIS_URL if not provided
  - CELERY_RESULT_BACKEND: Optional[str] = None  # default to REDIS_URL if not provided
  - BITBUCKET_WEBHOOK_SECRET: Optional[str] = None
  - HARNESS_WEBHOOK_SECRET: Optional[str] = None
  - OTEL_SERVICE_NAME: str = "sentinel-backend"
  - OTLP_ENDPOINT already present; keep default

6.2 Update .env.example
- Add the new variables above and brief comments


## 7) Observability (OpenTelemetry + Structlog)

7.1 FastAPI tracing
- Modify src/sentinel/main.py:
  - Initialize SDK:
    - TracerProvider(resource=Resource.create({"service.name": settings.OTEL_SERVICE_NAME}))
    - OTLPSpanExporter(endpoint=settings.OTLP_ENDPOINT)
    - BatchSpanProcessor(exporter)
  - Keep FastAPIInstrumentor.instrument_app(app)

7.2 Task tracing
- In src/sentinel/tasks/test_run_tasks.py, wrap major steps in spans using opentelemetry.trace.get_tracer("sentinel.tasks")

7.3 Logging
- Continue using structlog via src/sentinel/core/logging.py
- Bind run_id, commit_id, branch, and jira_ticket_id on logs in task and API layers


## 8) Minimal Frontend Integration (Optional for later)
- Expose GET /api/v1/test-runs and GET /api/v1/test-runs/{run_id}
- In frontend/src/App.tsx, replace the placeholder in the "Test Runs" tab with a fetch to list runs and display status


## 9) Security Notes
- Never echo webhook secrets in logs
- Restrict CORS in production in src/sentinel/main.py
- Validate inputs in API models (lengths, URL format)


## 10) Rollout Steps
1) Write code per the path references above
2) make format && make lint
3) Run alembic upgrade head
4) make docker-up (ensure redis/postgres running)
5) Start app: make dev
6) Start worker: docker-compose up worker
7) Manually POST to /api/v1/test-runs and validate lifecycle

---
