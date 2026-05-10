"""Command-line entry point for my-smart-project."""

from __future__ import annotations

from my_smart_project.cli import main
from my_smart_project.models import STATUS_MESSAGE, get_status_message

__all__ = ["STATUS_MESSAGE", "get_status_message", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
