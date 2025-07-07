# Task Completion Checklist

When you complete any coding task in the Sentinel project, ALWAYS:

## 1. Code Quality Checks (REQUIRED)
```bash
# Format the code
make format

# Run linting - MUST PASS
make lint
# or manually:
uv run ruff check src/ tests/
uv run mypy src/

# Run tests if applicable
make test
```

## 2. Verification Steps
- Ensure no linting errors or type checking issues
- Verify tests pass if you modified tested code
- Check that imports are properly sorted (isort)
- Confirm code follows 88-character line limit

## 3. Important Notes
- **NEVER** commit code that fails linting
- If you can't find lint/typecheck commands, ASK the user
- Suggest adding commands to CLAUDE.md for future reference
- The project uses strict mypy checking - all types must be proper

## 4. Pre-commit Hooks
The project has pre-commit hooks that will automatically check:
- Trailing whitespace
- File endings
- YAML/JSON/TOML validity
- Large file additions
- Debug statements
- Black formatting
- isort import ordering
- Ruff linting

If commits fail due to pre-commit hooks, the issues must be fixed before committing.