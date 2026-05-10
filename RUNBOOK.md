# Runbook

This runbook explains how to run and test the current minimal project locally.

## Requirements

- Python 3.10 or newer is recommended.
- No third-party Python packages are required.
- No secrets, API keys, credentials, or external services are required.

## Optional Virtual Environment

A virtual environment is optional because the project currently has no dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
```

## Run the CLI

From the repository root:

```bash
python -m src.main
```

Expected output:

```text
my-smart-project: minimal Codex-ready starter is working.
```

## Run Tests

From the repository root:

```bash
python -m unittest discover -s tests
```

Expected result:

```text
OK
```

The exact number of tests may change as the project grows.

## Troubleshooting

If Python cannot import `src.main`, confirm that the command is being run from the repository root.

If the command `python` does not work on your machine, try:

```bash
python3 -m src.main
python3 -m unittest discover -s tests
```

## Adding Dependencies Later

Do not add `requirements.txt` until the project needs at least one third-party package. When dependencies are added, document why each one is needed and update this runbook with installation steps.
