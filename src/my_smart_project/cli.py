"""Command-line interface for Saeid KING Content Command Center v1."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .content_workspace import (
    WorkspaceError,
    create_video_project,
    export_project_brief,
    init_workspace,
    list_video_projects,
    load_video_project,
    update_video_field,
    update_video_section_status,
    update_video_status,
)
from .models import ALLOWED_STATUSES, VideoProject, get_status_message


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="python3 -m src.main",
        description="Saeid KING Content Command Center v1: local video project records.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Print the project status message.")

    init_parser = subparsers.add_parser(
        "init-workspace",
        help="Create a local content workspace folder.",
    )
    init_parser.add_argument("--path", required=True, help="Workspace folder path to create.")

    new_video_parser = subparsers.add_parser(
        "new-video",
        help="Create a new video project JSON record.",
    )
    new_video_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    new_video_parser.add_argument("--slug", required=True, help="Safe project slug.")
    new_video_parser.add_argument("--title", required=True, help="Video project title.")

    list_parser = subparsers.add_parser(
        "list-videos",
        help="List video projects in a workspace.",
    )
    list_parser.add_argument("--workspace", required=True, help="Content workspace path.")

    overview_parser = subparsers.add_parser(
        "overview-videos",
        help="Show a compact workflow overview for video projects.",
    )
    overview_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    overview_parser.add_argument(
        "--status",
        choices=ALLOWED_STATUSES,
        help="Optional production status filter.",
    )

    show_parser = subparsers.add_parser(
        "show-video",
        help="Show one video project record.",
    )
    show_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    show_parser.add_argument("--slug", required=True, help="Project slug to show.")

    update_parser = subparsers.add_parser(
        "update-status",
        help="Update one video project's production status.",
    )
    update_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    update_parser.add_argument("--slug", required=True, help="Project slug to update.")
    update_parser.add_argument(
        "--status",
        required=True,
        choices=ALLOWED_STATUSES,
        help="New production status.",
    )

    field_parser = subparsers.add_parser(
        "update-field",
        help="Update one safe video project metadata field.",
    )
    field_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    field_parser.add_argument("--slug", required=True, help="Project slug to update.")
    field_parser.add_argument(
        "--field",
        required=True,
        help="Safe metadata field to update: core_question or notes.",
    )
    field_parser.add_argument("--value", required=True, help="New field value.")

    section_parser = subparsers.add_parser(
        "update-section-status",
        help="Update one safe video project section status.",
    )
    section_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    section_parser.add_argument("--slug", required=True, help="Project slug to update.")
    section_parser.add_argument(
        "--section",
        required=True,
        help="Section to update: research, script, broll, editing, or publishing.",
    )
    section_parser.add_argument(
        "--status",
        required=True,
        help="New section status: not_started, in_progress, blocked, or done.",
    )

    export_parser = subparsers.add_parser(
        "export-brief",
        help="Export a Markdown production brief for one project.",
    )
    export_parser.add_argument("--workspace", required=True, help="Content workspace path.")
    export_parser.add_argument("--slug", required=True, help="Project slug to export.")

    return parser


def format_video_list(projects: list[VideoProject]) -> str:
    """Return a readable table-like project list."""
    if not projects:
        return "No video projects found."

    rows = [("SLUG", "STATUS", "TITLE")]
    rows.extend((project.slug, project.status, project.title) for project in projects)
    widths = [max(len(row[index]) for row in rows) for index in range(3)]

    lines = [
        f"{rows[0][0]:<{widths[0]}}  {rows[0][1]:<{widths[1]}}  {rows[0][2]}",
        f"{'-' * widths[0]}  {'-' * widths[1]}  {'-' * widths[2]}",
    ]
    lines.extend(
        f"{slug:<{widths[0]}}  {status:<{widths[1]}}  {title}"
        for slug, status, title in rows[1:]
    )
    return "\n".join(lines)


def format_video_overview(projects: list[VideoProject]) -> str:
    """Return a compact table-like workflow overview."""
    if not projects:
        return "No video projects found."

    rows = [
        (
            "SLUG",
            "STATUS",
            "RESEARCH",
            "SCRIPT",
            "B-ROLL",
            "EDITING",
            "PUBLISHING",
            "TITLE",
        )
    ]
    rows.extend(
        (
            project.slug,
            project.status,
            project.research_status,
            project.script_status,
            project.broll_status,
            project.editing_status,
            project.publishing_status,
            project.title,
        )
        for project in projects
    )
    widths = [max(len(row[index]) for row in rows) for index in range(8)]

    lines = [
        (
            f"{rows[0][0]:<{widths[0]}}  {rows[0][1]:<{widths[1]}}  "
            f"{rows[0][2]:<{widths[2]}}  {rows[0][3]:<{widths[3]}}  "
            f"{rows[0][4]:<{widths[4]}}  {rows[0][5]:<{widths[5]}}  "
            f"{rows[0][6]:<{widths[6]}}  {rows[0][7]}"
        ),
        (
            f"{'-' * widths[0]}  {'-' * widths[1]}  {'-' * widths[2]}  "
            f"{'-' * widths[3]}  {'-' * widths[4]}  {'-' * widths[5]}  "
            f"{'-' * widths[6]}  {'-' * widths[7]}"
        ),
    ]
    lines.extend(
        (
            f"{slug:<{widths[0]}}  {status:<{widths[1]}}  "
            f"{research:<{widths[2]}}  {script:<{widths[3]}}  "
            f"{broll:<{widths[4]}}  {editing:<{widths[5]}}  "
            f"{publishing:<{widths[6]}}  {title}"
        )
        for slug, status, research, script, broll, editing, publishing, title in rows[1:]
    )
    return "\n".join(lines)


def format_video_detail(project: VideoProject) -> str:
    """Return readable details for one video project."""
    return "\n".join(
        [
            f"Title: {project.title}",
            f"Slug: {project.slug}",
            f"Status: {project.status}",
            f"Created At: {project.created_at}",
            f"Updated At: {project.updated_at}",
            f"Core Question: {project.core_question}",
            f"Research Status: {project.research_status}",
            f"Script Status: {project.script_status}",
            f"B-roll Status: {project.broll_status}",
            f"Editing Status: {project.editing_status}",
            f"Publishing Status: {project.publishing_status}",
            f"Notes: {project.notes}",
        ]
    )


def run_command(args: argparse.Namespace) -> str:
    """Run a parsed CLI command and return stdout text."""
    if args.command in (None, "status"):
        return get_status_message()
    if args.command == "init-workspace":
        return init_workspace(args.path)
    if args.command == "new-video":
        path = create_video_project(args.workspace, args.slug, args.title)
        return f"Created video project: {path}"
    if args.command == "list-videos":
        return format_video_list(list_video_projects(args.workspace))
    if args.command == "overview-videos":
        projects = list_video_projects(args.workspace)
        if args.status is not None:
            projects = [
                project for project in projects if project.status == args.status
            ]
        return format_video_overview(projects)
    if args.command == "show-video":
        return format_video_detail(load_video_project(args.workspace, args.slug))
    if args.command == "update-status":
        project = update_video_status(args.workspace, args.slug, args.status)
        return f"Updated {project.slug} status to {project.status}."
    if args.command == "update-field":
        project = update_video_field(args.workspace, args.slug, args.field, args.value)
        return f"Updated {project.slug} {args.field}."
    if args.command == "update-section-status":
        project = update_video_section_status(
            args.workspace, args.slug, args.section, args.status
        )
        return f"Updated {project.slug} {args.section} status to {args.status}."
    if args.command == "export-brief":
        path = export_project_brief(args.workspace, args.slug)
        return f"Exported brief: {path}"

    raise WorkspaceError(f"Unsupported command: {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    parsed_args = parser.parse_args(argv)

    try:
        output = run_command(parsed_args)
    except (ValueError, WorkspaceError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0
