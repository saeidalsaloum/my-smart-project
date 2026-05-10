"""Minimal CLI entry point for my-smart-project."""

STATUS_MESSAGE = "my-smart-project: minimal Codex-ready starter is working."


def get_status_message() -> str:
    """Return the current project status message."""
    return STATUS_MESSAGE


def main() -> None:
    """Print the project status message."""
    print(get_status_message())


if __name__ == "__main__":
    main()
