# Contributing to CRAB

Thank you for your interest in making CRAB better. This document covers how to contribute code, report issues, and suggest improvements.

## Quick Start

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feat/your-name/description`
4. Make your changes
5. Run the test suite: `python -m pytest tests/ -v`
6. Commit with a clear message following [Conventional Commits](https://www.conventionalcommits.org/)
7. Push and open a Pull Request

## Development Setup

CRAB is intentionally simple — it requires only Python 3.11+ and the standard library at runtime.

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python -m pytest tests/ -v
```

No runtime dependencies are needed. Development and test commands may use editable installs or test extras when validating packaging behavior.

## Code Standards

- **stdlib only**: No third-party dependencies in the core daemon
- **Type hints**: Add type annotations for new public functions
- **Docstrings**: Google-style docstrings for modules and public APIs
- **Tests**: Every bug fix and new feature must include a test
- **Backwards compatibility**: Public API changes require a deprecation cycle

## Commit Message Format

```
<type>: <short description>

<body> (optional)

<footer> (optional)
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

### Batch enhancement commits

When committing doc-enhance sweep batches, use the `crab(doc-enhance):` scope:

```
crab(doc-enhance): batch N — X T< tier > research docs

Enhanced X Tier-<tier> research documents with structured frontmatter,
evidence grades, confidence scores, DOI audit notes, bibliography
placeholders, and gaps/next-steps checklists.

Generated with [Devin](https://cli.devin.ai/docs)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
```

Example:
```
crab(doc-enhance): batch 14 — 20 T2 research docs
```

Example:
```
feat: add HTTP bus backend for webhook-style integration

Implements HttpBusBackend that POSTs messages to a configurable
endpoint. Includes retry with exponential backoff.

Closes #42
```

## Pull Request Process

1. PRs should be focused — one logical change per PR
2. Ensure all tests pass locally before pushing
3. Update `README.md` if your change affects the public API
4. Add an entry to `CHANGELOG.md` if one exists, or note the change in the PR description
5. Request review from a maintainer

## Reporting Issues

When reporting bugs, please include:

- Python version (`python --version`)
- Operating system and version
- Minimal reproduction steps
- Expected vs actual behavior
- If relevant, the output of `python -m pytest tests/ -v`

## Security Issues

Please do not open public issues for security vulnerabilities. Instead, email `security@hummbl.io` with details. We will respond within 48 hours.

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Questions?

Open a [Discussion](https://github.com/hummbl-dev/crab/discussions) or ask in the PR — we're happy to help.
