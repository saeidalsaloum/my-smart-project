# my-smart-project

`my-smart-project` is a local, public-safe Python CLI for organizing generic video production work.

Phase 2 introduced **Saeid KING Content Command Center v1**: a minimal command-line tool for creating local content workspaces, storing simple video project records as JSON, and exporting safe Markdown production briefs. Phase 3A added narrow local editing for approved safe metadata fields. Phase 3B adds narrow section status editing.

The project remains deliberately conservative. It does not connect to YouTube, Google, OpenAI, GitHub, databases, cloud services, paid tools, analytics systems, or deployment platforms.

## Current Status

- Project type: local Python CLI
- Runtime: Python standard library only
- Data storage: local JSON files in a user-chosen workspace
- External services: none
- Secrets required: none
- Deployment: none
- Default development model: reviewable branches and draft pull requests

## What It Does Today

The CLI can:

- Print the project status message.
- Initialize a local content workspace.
- Create simple video project JSON records.
- List video project records.
- Show one project record.
- Update a project's production status.
- Update a project's `core_question` or `notes` field.
- Update a project's section status fields for research, script, B-roll, editing, and publishing workflow steps.
- Export a Markdown production brief with safe metadata and section statuses.

All records use generic fields only. Do not store real private analytics, legal material, personal data, credentials, or sensitive production files in this repository or in example workspace data.

## Quick Start

Clone the repository and enter the project directory:

```bash
git clone https://github.com/saeidalsaloum/my-smart-project.git
cd my-smart-project
```

Show help:

```bash
python3 -m src.main --help
```

Check project status:

```bash
python3 -m src.main status
```

Initialize a local content workspace:

```bash
python3 -m src.main init-workspace --path ./content-workspace
```

Create a video project:

```bash
python3 -m src.main new-video \
  --workspace ./content-workspace \
  --slug first-video \
  --title "First Video"
```

List projects:

```bash
python3 -m src.main list-videos --workspace ./content-workspace
```

Show one project:

```bash
python3 -m src.main show-video --workspace ./content-workspace --slug first-video
```

Update status:

```bash
python3 -m src.main update-status \
  --workspace ./content-workspace \
  --slug first-video \
  --status editing
```

Update the core question:

```bash
python3 -m src.main update-field \
  --workspace ./content-workspace \
  --slug first-video \
  --field core_question \
  --value "Why does this topic matter?"
```

Update notes:

```bash
python3 -m src.main update-field \
  --workspace ./content-workspace \
  --slug first-video \
  --field notes \
  --value "Draft notes here."
```

Update a section status:

```bash
python3 -m src.main update-section-status \
  --workspace ./content-workspace \
  --slug first-video \
  --section research \
  --status in_progress
```

Export a brief:

```bash
python3 -m src.main export-brief --workspace ./content-workspace --slug first-video
```

The exported brief includes the project title, safe project metadata (`slug`,
production `status`, `created_at`, and `updated_at`), the five section statuses,
the core question, and empty production-planning sections. It does not export
`notes`, private paths, credentials, diagnostics, or other system fields.

Run tests:

```bash
python3 -m unittest discover -s tests
```

No package installation is required.

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
|   |-- main.py
|   `-- my_smart_project/
|       |-- __init__.py
|       |-- cli.py
|       |-- content_workspace.py
|       `-- models.py
`-- tests/
    `-- test_main.py
```

## Safety Model

This repository is intentionally conservative:

- No secrets, credentials, tokens, private data, or sensitive documents belong in the repository.
- No real YouTube analytics exports, legal material, personal files, media folders, or private production archives should be added.
- No external service integrations are present.
- No paid services, AI APIs, databases, deployment systems, or analytics tools are configured.
- Workspace initialization refuses unsafe existing paths and does not overwrite existing project files or exported briefs.
- Field editing is limited to `core_question` and `notes` and rewrites only the selected project JSON file.
- Section status editing is limited to approved section names and approved section status values, and rewrites only the selected project JSON file.
- Brief export includes only safe project metadata, section statuses, the core question, and production-planning headings.
- New architecture should be documented before implementation.

## Development Workflow

1. Start from an issue, written request, or documented project decision.
2. Create or update a review branch; do not push directly to `main`.
3. Keep the change small and aligned with `docs/PROJECT_PLAN.md`.
4. Update documentation when behavior, commands, scope, or safety rules change.
5. Run the CLI smoke checks and tests before requesting review.
6. Keep pull requests in draft until the human owner decides they are ready.

## Testing

The test suite uses Python `unittest` from the standard library.

```bash
python3 -m src.main --help
python3 -m src.main status
python3 -m unittest discover -s tests
```

The GitHub Actions workflow runs CLI smoke checks and `unittest` on `push` and `pull_request`. It does not deploy, publish, or require secrets.

## Documentation

- `AGENTS.md`: operating rules for Codex and automation-assisted changes.
- `RUNBOOK.md`: local run, test, verification, and troubleshooting steps.
- `docs/PROJECT_PLAN.md`: confirmed scope, non-goals, risks, open decisions, and next milestone.
- `docs/DEVELOPMENT_GUIDE.md`: contribution and review workflow.
- `docs/SECURITY.md`: concise security and privacy rules.

## Next Milestone

Continue the local-only workflow carefully: review whether brief export content should incorporate the new safe metadata and section statuses.
