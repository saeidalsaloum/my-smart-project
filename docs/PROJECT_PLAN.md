# Project Plan

## Purpose

`my-smart-project` is a safe foundation for local, AI-assisted software development around public-safe video production workflows.

Phase 2 introduces the first real capability: Saeid KING Content Command Center v1, a local CLI for managing simple video project records in JSON and exporting Markdown briefs. The tool is intentionally generic and safe for a public repository.

## Confirmed Current Scope

The repository currently provides:

- A Python CLI entry point at `python3 -m src.main`.
- A status command and backward-compatible no-command status output.
- Local workspace initialization with `projects/`, `exports/`, and workspace `README.md`.
- Simple video project JSON records with safe generic fields only.
- Project listing, detail display, status updates, and Markdown brief export.
- Standard-library `unittest` coverage for CLI behavior and workspace operations.
- A GitHub Actions workflow that runs tests on `push` and `pull_request` without secrets or deployment.

## Explicit Non-Goals

The project is not currently:

- A web application.
- An API service.
- A database-backed system.
- A deployment target.
- An AI API integration.
- A YouTube, Google, OpenAI, GitHub, cloud, or paid-service integration.
- A real analytics processor.
- A media processing pipeline.
- A customer data system.
- A legal, personal, or private document repository.

Do not add those capabilities without a documented decision and explicit approval.

## Phase Status

### Phase 1: Professional Foundation

Status: complete.

Exit criteria met:

- Local CLI command works.
- Local tests pass.
- GitHub Actions test workflow is present.
- Security and privacy boundaries are documented.
- No third-party dependencies are required.

### Phase 2: Content Command Center v1

Status: in implementation.

Goal:

Create a useful local CLI for generic video production project records without connecting to external services or storing private data.

Exit criteria:

- `--help` and `status` commands work.
- Workspace initialization is safe and non-destructive.
- New video project JSON files are created with the approved field schema.
- Project listing, show, status update, and brief export commands work.
- Invalid status, missing project, duplicate project, unsafe workspace, and existing brief cases are handled clearly.
- Tests cover the required workflows.
- Documentation reflects actual behavior.

### Phase 3: Focused Field Editing

Potential next milestone:

Add small commands for editing safe project fields such as `core_question`, `notes`, and section statuses. This should remain local-only and standard-library-only.

### Phase 4: Architecture Decision

Only after repeated real local use, decide whether the project needs packaging, richer validation, import/export formats, or stronger quality tooling.

## Data Model

Each video project JSON file contains exactly these fields:

- `slug`
- `title`
- `status`
- `created_at`
- `updated_at`
- `core_question`
- `research_status`
- `script_status`
- `broll_status`
- `editing_status`
- `publishing_status`
- `notes`

Default production status is `idea`. Section statuses default to `not_started`. Timestamps use UTC ISO format ending in `Z`.

## Risks

- Secret leakage: committing `.env` files, tokens, keys, credentials, private exports, or real analytics.
- Scope drift: turning the CLI into a web app, service integration, or media pipeline too early.
- False capability claims: documenting production features that the code does not actually provide.
- Overwriting user work: regenerating project files or briefs over manual edits.
- Premature architecture: adding frameworks, databases, services, or dependencies before the local workflow proves useful.
- Public repository safety: accidentally adding real personal, legal, YouTube, media, or business material.

## Open Decisions

- Whether the next feature should edit project fields, add checklist status commands, or improve brief content.
- Whether local workspace records should later support schema versions.
- Whether packaging is useful after the CLI stabilizes.
- Whether additional quality tools are worth adding while keeping dependencies minimal.

## Next Milestone

After v1 is reviewed, choose one narrow command for editing safe project metadata. The likely candidate is a command that updates `core_question` or `notes` without changing the repository's local-only safety model.

## Decision Rule

If a proposed change requires a framework, external service, paid tool, private data, deployment configuration, database, AI API, or new dependency, document the decision first and ask for explicit approval before implementation.
