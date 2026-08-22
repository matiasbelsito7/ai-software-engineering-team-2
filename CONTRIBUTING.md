# Contributing to AI Software Engineering Team

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Install dependencies: `make install`
5. Make your changes
6. Run quality checks: `make check`
7. Commit and push

## Development Workflow

### Setup

```bash
make install        # Install all dependencies
make install-hooks  # Install pre-commit hooks
```

### Before Every Commit

```bash
make check   # format-check + lint + typecheck + test
```

This ensures your code passes all quality gates before pushing.

### Code Style

- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type Checker**: mypy (strict mode)
- Follow existing patterns in the codebase

### Testing

```bash
make test           # Run all tests
make test-unit      # Unit tests only
make test-integration  # Integration tests only
```

- Write tests for new features and bug fixes
- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Aim for meaningful coverage, not just high numbers

### Project Structure

```
src/ai_team/
├── agents/          # AI agents (each in its own subpackage)
├── app/api/         # FastAPI application (routers, schemas, middleware)
├── graph/           # LangGraph workflow
├── tools/           # Agent tools (each tool in its own subpackage)
├── rag/             # Retrieval-Augmented Generation
├── memory/          # Agent memory
├── context/         # Context management
├── observability/   # Tracing and metrics
├── evals/           # Evaluation framework
└── infrastructure/  # Config, DI container, LLM providers
```

### Adding a New Agent

1. Create `src/ai_team/agents/myagent/` with:
   - `__init__.py`
   - `agent.py` (subclass `BaseAgent`)
   - `models.py` (output model)
   - `prompt_builder.py` (subclass `BasePromptBuilder`)
   - `prompts/system.md` and `prompts/task.md`
2. Register in `src/ai_team/infrastructure/container.py`
3. Add to the workflow in `src/ai_team/graph/builder.py`
4. Write tests in `tests/unit/` and `tests/integration/`

### Adding a New Tool

1. Create `src/ai_team/tools/mytool/` with:
   - `__init__.py` (export the tool class)
   - Tool implementation (subclass `BaseTool`)
2. Register in `src/ai_team/tools/factory.py`
3. Write tests in `tests/unit/test_tools.py`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure `make check` passes
4. Write a clear PR description explaining the change
5. Link any related issues

## Reporting Issues

- Use GitHub Issues
- Include steps to reproduce
- Include expected vs actual behavior
- Include Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
