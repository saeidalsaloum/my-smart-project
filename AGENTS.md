# AGENTS.md

These instructions apply to the whole repository.

## Mission

Work on `my-smart-project` as a small, safe, reviewable starter project. The project is not yet a large application. Preserve clarity, reversibility, and documentation before expanding scope.

## Non-Negotiable Safety Rules

- Do not delete files unless the user explicitly approves the exact deletion.
- Do not commit secrets, API keys, passwords, tokens, credentials, private personal data, or generated sensitive data.
- Do not connect the project to external services without explicit approval.
- Do not install dependencies unless they are clearly needed and approved.
- Do not make large architectural decisions without documenting the decision and tradeoffs first.
- Do not push directly to `main` unless the user explicitly requests it.
- Prefer a reviewable branch or pull request for changes.
- Keep changes small, readable, and easy to review.

## Coding Standards

- Prefer Python standard library features until a dependency is justified.
- Keep CLI behavior simple and deterministic.
- Keep tests focused on observable behavior.
- Use clear names and short files.
- Avoid clever abstractions before there is real complexity.

## Documentation Expectations

When changing behavior, update the relevant documentation:

- `README.md` for project overview and quick start.
- `RUNBOOK.md` for local run and test commands.
- `docs/PROJECT_PLAN.md` for scope, phases, risks, and next steps.

## Verification

Before reporting work as complete:

- Inspect the changed files.
- Run the smallest relevant test command when possible.
- State clearly if tests were not run.
- Summarize every file created or modified.

## Protected Boundaries

The following must not be added without explicit approval:

- Secrets or environment-specific credentials.
- Production deployment configuration.
- External database, cloud, payment, analytics, email, or AI service integrations.
- Large framework scaffolds.
- Generated binary assets.
