"""Command-line entry point for my-smart-project."""

from __future__ import annotations

PROJECT_NAME = "my-smart-project"
STATUS_MESSAGE = f"{PROJECT_NAME}: minimal Codex-ready starter is working."


def get_status_message() -> str:
    """Return the deterministic project status message."""
    return STATUS_MESSAGE


def main() -> int:
    """Run the CLI and return a process exit code."""
    print(get_status_message())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
