# Development Guide

This guide describes how to make small, reviewable changes to `my-smart-project` without expanding scope prematurely.

## Working Principles

- Keep changes narrow and easy to review.
- Prefer the Python standard library.
- Update tests when behavior changes.
- Update documentation when commands, scope, or safety rules change.
- Avoid broad architecture until the product direction is documented.

## Branch Workflow

1. Start from `main` or from the active draft PR branch if the work continues an existing change.
2. Use a branch name beginning with `codex/` for Codex-assisted work.
3. Keep the pull request draft until the human owner asks to mark it ready.
4. Do not merge automatically.

## Local Verification

Run these commands before review:

```bash
python3 -m src.main
python3 -m unittest discover -s tests
```

The CLI output should be:

```text
my-smart-project: minimal Codex-ready starter is working.
```

## Code Guidelines

- Keep CLI behavior deterministic.
- Return explicit exit codes from entry points when useful.
- Put tests under `tests/`.
- Use clear names over abstractions.
- Do not add dependencies unless the need is documented and approved.

## Documentation Guidelines

Use the smallest document that fits the change:

- `README.md` for repository overview and quick start.
- `RUNBOOK.md` for run, test, and troubleshooting steps.
- `docs/PROJECT_PLAN.md` for scope and future decisions.
- `docs/SECURITY.md` for privacy and secret-handling rules.
- `AGENTS.md` for Codex operating rules.

## Review Checklist

Before asking for review, confirm:

- Commands in the docs match actual behavior.
- Tests pass locally or the reason they could not run is documented.
- No secrets or private data were added.
- No unrelated files were added.
- No external service, deployment, or paid tool configuration was introduced.
