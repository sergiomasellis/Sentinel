# Sentinel Project Overview

**Sentinel** is an AI-driven testing platform that automatically generates, executes, and self-heals tests based on code changes and requirements.

## Core Capabilities
- **AI-Powered Test Generation**: Automatically creates E2E (Cypress), integration (pytest), and regression tests based on code changes
- **Self-Healing Tests**: Automatically fixes failing tests when selectors change or assertions need updating
- **Multi-Source Context**: Integrates with Bitbucket (code), Jira (requirements), Harness CI, and AWS ECS
- **Event-Driven Architecture**: Webhook-triggered workflow from CI/CD systems
- **Parallel Test Execution**: Runs tests concurrently for faster feedback
- **Comprehensive Observability**: OpenTelemetry instrumentation with Arize Phoenix for LLM monitoring

## Architecture Flow
1. Webhook triggers from CI/CD notify of code changes
2. Test Orchestrator fetches context (code diffs, Jira tickets)
3. AI Agent generates appropriate tests based on changes
4. Test Runner executes tests in parallel
5. Self-Healing Agent fixes failing tests automatically
6. Results are reported back to PR/Jira and monitoring systems

## Key Components
- **Backend Orchestrator**: FastAPI service managing test lifecycle
- **AI Agents**: LangChain/LangGraph powered test generation using Azure OpenAI
- **Frontend Dashboard**: React + TypeScript UI for monitoring and management
- **Integrations**: Bitbucket, Jira, Harness CI, AWS ECS connectors