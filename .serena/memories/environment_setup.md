# Environment Setup

## Required Environment Variables (.env file)

### Azure OpenAI Configuration
- `AZURE_OPENAI_API_KEY` - API key for Azure OpenAI
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Model deployment name

### Database Configuration
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

### External Service Credentials
- `BITBUCKET_USER` - Bitbucket username
- `BITBUCKET_APP_PASSWORD` - Bitbucket app password
- `JIRA_SERVER` - Jira instance URL
- `JIRA_EMAIL` - Jira user email
- `JIRA_API_TOKEN` - Jira API token

### AWS Configuration (if using ECS)
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region

### Application Settings
- `ENV` - Environment (development/staging/production)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)
- `CELERY_BROKER_URL` - Celery broker URL (usually same as REDIS_URL)

## Local Development Setup
1. Copy `.env.example` to `.env`
2. Fill in all required credentials
3. Start Docker services: `make docker-up`
4. Install dependencies: `make install`
5. Run migrations (when implemented)
6. Start development server: `make dev`

## Pre-commit Hooks
Install hooks to ensure code quality:
```bash
uv run pre-commit install
```