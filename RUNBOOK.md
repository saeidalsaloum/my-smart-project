# Runbook

This runbook explains how to clone, run, test, and verify Saeid KING Content Command Center v1 locally.

## Requirements

- Python 3.10 or newer is recommended.
- Git is required only for cloning the repository.
- No third-party Python packages are required.
- No secrets, API keys, credentials, paid accounts, or external services are required.

## Clone the Repository

```bash
git clone https://github.com/saeidalsaloum/my-smart-project.git
cd my-smart-project
```

If you are reviewing a pull request branch, check out the branch named in the PR before running commands:

```bash
git checkout <branch-name>
```

## Optional Virtual Environment

The project currently has no dependencies, so a virtual environment is optional.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Deactivate it later with:

```bash
deactivate
```

## CLI Smoke Checks

Show help:

```bash
python3 -m src.main --help
```

Print the status message:

```bash
python3 -m src.main status
```

Expected status output:

```text
my-smart-project: minimal Codex-ready starter is working.
```

Running without a command is kept as a backward-compatible status alias:

```bash
python3 -m src.main
```

## Local Content Workspace Example

Create a safe local workspace:

```bash
python3 -m src.main init-workspace --path ./content-workspace
```

This creates:

```text
content-workspace/
|-- README.md
|-- exports/
`-- projects/
```

If the workspace already exists and is valid, the command exits successfully with a helpful message. If the path exists but is not a valid workspace, the command refuses to modify it.

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

Allowed statuses:

```text
idea research script recording editing review scheduled published archived
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

Only `core_question` and `notes` are editable through `update-field`. The command updates `updated_at`, preserves the rest of the project schema, and does not rewrite exported briefs.

Update a section status:

```bash
python3 -m src.main update-section-status \
  --workspace ./content-workspace \
  --slug first-video \
  --section research \
  --status in_progress
```

Allowed sections:

```text
research script broll editing publishing
```

Allowed section status values:

```text
not_started in_progress blocked done
```

`update-section-status` updates only the mapped section status field, updates `updated_at`, preserves the rest of the project schema, and does not rewrite exported briefs.

Export a Markdown brief:

```bash
python3 -m src.main export-brief --workspace ./content-workspace --slug first-video
```

The brief is written to:

```text
content-workspace/exports/first-video_brief.md
```

Existing project JSON files and existing brief files are not overwritten.

## Run Tests

From the repository root:

```bash
python3 -m unittest discover -s tests
```

Expected result:

```text
OK
```

The exact number of tests may change as the project grows.

## Verify a Local Change

Use this sequence before asking for review:

```bash
python3 -m src.main --help
python3 -m src.main status
python3 -m unittest discover -s tests
```

Then inspect the changed files and confirm that documentation still matches actual behavior.

## Troubleshooting

### `python3` is not found

Install Python 3.10 or newer, then rerun the commands. On some systems the command may be `python` instead of `python3`.

### `No module named src.main`

Run the command from the repository root. The command expects the `src/` directory to be in the current working directory.

### Workspace path is refused

The CLI uses a strict-safe workspace policy. If the path exists but does not contain `projects/`, `exports/`, and `README.md`, choose a new path or manually create a valid workspace structure.

### Project already exists

`new-video` never overwrites an existing `<slug>.json` file. Use a new slug or review the existing project file manually.

### Field is not supported

`update-field` only accepts `core_question` and `notes`. Other metadata, status fields, timestamps, and identifiers are intentionally protected from this command.

### Section or section status is not supported

`update-section-status` only accepts the approved sections and section status values listed above. Project identifiers, title, production status, metadata fields, timestamps, and unrelated section statuses are intentionally protected from this command.

### Project file is invalid

Project JSON files with missing fields, unexpected fields, invalid production statuses, or invalid stored section statuses are rejected. The CLI does not repair, normalize, or rewrite invalid project JSON automatically.

### Brief already exists

`export-brief` never overwrites an existing Markdown brief. Remove or rename the existing brief manually before exporting again.

## Dependency Policy

There is intentionally no `requirements.txt` because the project has no third-party dependencies. Add dependency files only after a dependency is approved and documented.
