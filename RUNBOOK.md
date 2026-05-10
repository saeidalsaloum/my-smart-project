# Runbook

This runbook explains how to clone, run, test, and verify the current minimal project locally.

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

If you are reviewing a pull request branch, check it out before running commands:

```bash
git checkout codex/minimal-starter
```

## Optional Virtual Environment

The project currently has no dependencies, so a virtual environment is optional. It can still be useful to keep local Python work isolated.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Deactivate it later with:

```bash
deactivate
```

## Run the CLI

From the repository root:

```bash
python3 -m src.main
```

Expected output:

```text
my-smart-project: minimal Codex-ready starter is working.
```

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
python3 -m src.main
python3 -m unittest discover -s tests
```

Then inspect the changed files and confirm that documentation still matches actual behavior.

## Troubleshooting

### `python3` is not found

Install Python 3.10 or newer, then rerun the commands. On some systems the command may be `python` instead of `python3`.

### `No module named src.main`

Run the command from the repository root. The command expects the `src/` directory to be in the current working directory.

### Tests fail after changing the status message

Update both the implementation and the expected value in `tests/test_main.py`. The test intentionally locks the CLI's observable output.

### GitHub Actions fails but local tests pass

Check that the workflow is running the same command documented here:

```bash
python3 -m unittest discover -s tests
```

If the commands diverge, update the documentation or the workflow so they match.

## Dependency Policy

There is intentionally no `requirements.txt` because the project has no third-party dependencies. Add dependency files only after a dependency is approved and documented.
