# my-smart-project

`my-smart-project` is a deliberately small Python starter repository prepared for safe, reviewable, AI-assisted development with Codex.

The project is not a production application yet. Its current purpose is to establish a clean baseline: documented scope, deterministic behavior, standard-library-only tests, and strict operating rules before larger decisions are made.

## Current Status

- Project type: minimal Python CLI foundation
- Runtime: Python standard library only
- External services: none
- Secrets required: none
- Deployment: none
- Default development model: reviewable branches and draft pull requests

## What It Does Today

The CLI prints a single deterministic status message so the repository has a known runnable behavior and a testable contract.

```bash
python3 -m src.main
```

Expected output:

```text
my-smart-project: minimal Codex-ready starter is working.
```

## Quick Start

Clone the repository and enter the project directory:

```bash
git clone https://github.com/saeidalsaloum/my-smart-project.git
cd my-smart-project
```

Run the CLI:

```bash
python3 -m src.main
```

Run the tests:

```bash
python3 -m unittest discover -s tests
```

No package installation is required for the current project state.

## Project Layout

```text
.
|-- .github/workflows/tests.yml
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- RUNBOOK.md
|-- docs/
|   |-- DEVELOPMENT_GUIDE.md
|   |-- PROJECT_PLAN.md
|   `-- SECURITY.md
|-- pyproject.toml
|-- src/
|   `-- main.py
`-- tests/
    `-- test_main.py
```

## Safety Model

This repository is intentionally conservative:

- No secrets, credentials, tokens, private data, or sensitive documents belong in the repository.
- No external service integrations are present.
- No paid services, AI APIs, databases, deployment systems, or analytics tools are configured.
- New architecture should be documented before implementation.
- Changes should be small enough to review directly in a pull request.

## Development Workflow

1. Start from an issue, written request, or documented project decision.
2. Create or update a review branch; do not push directly to `main`.
3. Keep the change small and aligned with `docs/PROJECT_PLAN.md`.
4. Update documentation when behavior, commands, scope, or safety rules change.
5. Run the CLI and tests before requesting review.
6. Keep pull requests in draft until the human owner decides they are ready.

## Testing

The test suite uses Python `unittest` from the standard library.

```bash
python3 -m unittest discover -s tests
```

The GitHub Actions workflow runs the same test command on `push` and `pull_request`. It does not deploy, publish, or require secrets.

## Documentation

- `AGENTS.md`: operating rules for Codex and automation-assisted changes.
- `RUNBOOK.md`: local run, test, verification, and troubleshooting steps.
- `docs/PROJECT_PLAN.md`: confirmed scope, non-goals, risks, open decisions, and next milestone.
- `docs/DEVELOPMENT_GUIDE.md`: contribution and review workflow.
- `docs/SECURITY.md`: concise security and privacy rules.

## Next Milestone

Define the first real product capability in one paragraph, then implement the smallest testable version without adding frameworks, external services, or broad architecture prematurely.
