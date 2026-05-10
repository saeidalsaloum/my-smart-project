"""Command-line interface for Saeid KING Content Command Center v1."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .models import STATUS_MESSAGE, get_status_message


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="my-smart-project",
        description="Local, public-safe content command center starter.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Print the current project status message.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = list(argv) if argv is not None else []

    if not args:
        print(get_status_message())
        return 0

    parser = build_parser()
    namespace = parser.parse_args(args)

    if namespace.command == "status":
        print(get_status_message())
        return 0

    parser.print_help()
    return 0
