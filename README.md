# my-smart-project

A safe, minimal starter project for AI-assisted development with Codex.

The repository is intentionally small. Its current purpose is to provide a clear, reviewable foundation before any larger application, external integration, or architectural commitment is made.

## Current Status

- Project type: minimal Python CLI starter
- Runtime dependencies: none beyond Python standard library
- External services: none
- Secrets required: none
- Intended workflow: small changes on reviewable branches

## Repository Layout

```text
.
├── AGENTS.md
├── README.md
├── RUNBOOK.md
├── docs/
│   └── PROJECT_PLAN.md
├── src/
│   └── main.py
└── tests/
    └── test_main.py
```

## Quick Start

Run the CLI from the repository root:

```bash
python -m src.main
```

Run the test suite:

```bash
python -m unittest discover -s tests
```

## Development Principles

- Keep the project small until the real product scope is documented.
- Avoid secrets, credentials, tokens, or private personal data in the repository.
- Avoid unnecessary dependencies.
- Prefer reviewable branches or pull requests over direct changes to `main`.
- Document architectural decisions before implementing them.

## Next Step

Use `docs/PROJECT_PLAN.md` and `RUNBOOK.md` as the baseline for deciding what this project should become next.
