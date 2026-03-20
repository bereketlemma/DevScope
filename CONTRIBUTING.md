# Contributing to DevScope

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
make install
make dev
```

## Style Guidelines

- Python: Follow PEP 8, enforced by `ruff` and `black`
- TypeScript: Follow ESLint configuration
- Commit messages: Conventional commits format

## Before Submitting

1. Run tests: `make test`
2. Format code: `make format`
3. Lint code: `make lint`
4. Type check: `make type-check`

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit using conventional commits
4. Push to your fork
5. Open a pull request with a clear description

## Code Review

All PRs are reviewed for:
- Code quality and style
- Test coverage
- Documentation
- Performance implications

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
