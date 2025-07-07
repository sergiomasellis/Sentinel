# API Endpoints

## Health & Status
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health with dependency checks

## Test Runs
- `POST /api/v1/test-runs` - Create new test run
  - Body: Test configuration, target branch, context
  - Returns: Test run ID and initial status
  
- `GET /api/v1/test-runs/{run_id}` - Get test run status
  - Returns: Current status, results, logs
  
- `GET /api/v1/test-runs` - List test runs with filtering
  - Query params: status, branch, date range

## Webhooks
- `POST /api/v1/webhooks/bitbucket` - Bitbucket events
  - Handles: PR created/updated, commits pushed
  - Triggers: Test generation for code changes
  
- `POST /api/v1/webhooks/harness` - Harness CI events
  - Handles: Pipeline status updates
  - Triggers: Test execution in CI environment

## Future Endpoints (Planned)
- Test results visualization
- Self-healing status and history
- Configuration management
- User management and authentication

## API Conventions
- RESTful design patterns
- JSON request/response bodies
- Proper HTTP status codes
- Structured error responses
- Request ID tracking for debugging