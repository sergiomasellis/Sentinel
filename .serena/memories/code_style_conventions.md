# Code Style and Conventions

## Python Code Style
- **Line Length**: 88 characters (Black standard)
- **Python Version**: 3.12+ with modern type hints
- **Formatting**: Black (automatic formatting)
- **Import Sorting**: isort with Black profile
- **Type Checking**: mypy in strict mode

## Linting Configuration (Ruff)
- **Selected Rules**: E, F, I, N, UP, B, C4, DTZ, T20, PT, RET, SIM
- **Ignored**: E501 (line length handled by Black), B008
- **Test Files**: Ignore S101 (assert statements allowed in tests)

## TypeScript/React Conventions
- **Framework**: React with TypeScript strict mode
- **Components**: Functional components with hooks
- **Styling**: Tailwind utility classes
- **UI Components**: shadcn/ui pattern with class-variance-authority

## General Conventions
- **Async First**: Use async/await for all database operations
- **Structured Logging**: Use `get_logger(__name__)` from core.logging
- **API Design**: RESTful endpoints with FastAPI
- **Error Handling**: Proper exception handling with meaningful messages
- **Testing**: pytest with async support, aim for high coverage

## File Organization
- Backend modules in `src/sentinel/`
- Clear separation: api/, models/, services/, agents/, integrations/
- Frontend components in `frontend/src/components/`
- Tests mirror source structure in `tests/`