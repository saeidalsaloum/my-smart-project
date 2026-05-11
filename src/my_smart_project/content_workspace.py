"""Local workspace operations for video project records."""

from __future__ import annotations

import json
from pathlib import Path

from .models import VideoProject, next_utc_iso_after, validate_slug, validate_status

PROJECTS_DIR = "projects"
EXPORTS_DIR = "exports"
WORKSPACE_README = "README.md"

WORKSPACE_README_CONTENT = """# Saeid KING Content Workspace

This local workspace stores generic video production project records.

Safe-use rules:

- Do not store secrets, API keys, credentials, or tokens here.
- Do not store private personal data, legal documents, or analytics exports here.
- Keep project records generic and suitable for a public repository workflow.
"""


class WorkspaceError(RuntimeError):
    """Raised when a workspace operation cannot be completed safely."""


def workspace_path(path: str) -> Path:
    """Return a normalized workspace path."""
    return Path(path).expanduser()


def projects_dir(workspace: Path) -> Path:
    """Return the projects directory for a workspace."""
    return workspace / PROJECTS_DIR


def exports_dir(workspace: Path) -> Path:
    """Return the exports directory for a workspace."""
    return workspace / EXPORTS_DIR


def is_valid_workspace(workspace: Path) -> bool:
    """Return whether a path already has the expected workspace structure."""
    return (
        workspace.is_dir()
        and projects_dir(workspace).is_dir()
        and exports_dir(workspace).is_dir()
        and (workspace / WORKSPACE_README).is_file()
    )


def ensure_workspace(path: str) -> Path:
    """Return a valid workspace path or raise a helpful error."""
    workspace = workspace_path(path)
    if not is_valid_workspace(workspace):
        raise WorkspaceError(f"Not a valid content workspace: {workspace}")
    return workspace


def init_workspace(path: str) -> str:
    """Create a content workspace, or report that a valid one already exists."""
    workspace = workspace_path(path)

    if workspace.exists():
        if is_valid_workspace(workspace):
            return f"Content workspace already exists: {workspace}"
        raise WorkspaceError(
            f"Path exists but is not a valid content workspace: {workspace}"
        )

    workspace.mkdir(parents=True)
    projects_dir(workspace).mkdir()
    exports_dir(workspace).mkdir()
    (workspace / WORKSPACE_README).write_text(WORKSPACE_README_CONTENT, encoding="utf-8")
    return f"Created content workspace: {workspace}"


def project_file(workspace: Path, slug: str) -> Path:
    """Return the JSON path for a project slug."""
    validate_slug(slug)
    return projects_dir(workspace) / f"{slug}.json"


def create_video_project(workspace_path_value: str, slug: str, title: str) -> Path:
    """Create a new video project JSON file without overwriting."""
    workspace = ensure_workspace(workspace_path_value)
    project = VideoProject.create(slug=slug, title=title)
    path = project_file(workspace, slug)

    if path.exists():
        raise WorkspaceError(f"Video project already exists: {path}")

    path.write_text(json.dumps(project.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def load_video_project(workspace_path_value: str, slug: str) -> VideoProject:
    """Load one video project by slug."""
    workspace = ensure_workspace(workspace_path_value)
    path = project_file(workspace, slug)
    if not path.exists():
        raise WorkspaceError(f"Video project not found: {slug}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceError(f"Project file is not valid JSON: {path}") from exc

    if not isinstance(data, dict):
        raise WorkspaceError(f"Project file must contain a JSON object: {path}")

    try:
        return VideoProject.from_dict(data)
    except ValueError as exc:
        raise WorkspaceError(f"Invalid project file {path}: {exc}") from exc


def save_video_project(workspace_path_value: str, project: VideoProject) -> Path:
    """Save an existing project JSON file."""
    workspace = ensure_workspace(workspace_path_value)
    path = project_file(workspace, project.slug)
    if not path.exists():
        raise WorkspaceError(f"Video project not found: {project.slug}")

    path.write_text(json.dumps(project.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def list_video_projects(workspace_path_value: str) -> list[VideoProject]:
    """Return all video projects sorted by slug."""
    workspace = ensure_workspace(workspace_path_value)
    projects = [
        load_video_project(str(workspace), path.stem)
        for path in sorted(projects_dir(workspace).glob("*.json"))
    ]
    return sorted(projects, key=lambda project: project.slug)


def update_video_status(workspace_path_value: str, slug: str, status: str) -> VideoProject:
    """Update one project's production status."""
    validate_status(status)
    project = load_video_project(workspace_path_value, slug)
    project.status = status
    project.updated_at = next_utc_iso_after(project.updated_at)
    save_video_project(workspace_path_value, project)
    return project


def export_project_brief(workspace_path_value: str, slug: str) -> Path:
    """Export a Markdown brief for one project without overwriting."""
    workspace = ensure_workspace(workspace_path_value)
    project = load_video_project(workspace_path_value, slug)
    output_path = exports_dir(workspace) / f"{project.slug}_brief.md"

    if output_path.exists():
        raise WorkspaceError(f"Brief already exists and was not overwritten: {output_path}")

    output_path.write_text(render_project_brief(project), encoding="utf-8")
    return output_path


def render_project_brief(project: VideoProject) -> str:
    """Render a safe Markdown production brief."""
    return f"""# {project.title}

- Slug: `{project.slug}`
- Status: `{project.status}`

## Production Checklist

- [ ] Core question is clear
- [ ] Claims are verified
- [ ] Script notes are reviewed
- [ ] B-roll plan is drafted
- [ ] Thumbnail ideas are drafted
- [ ] Publishing checklist is complete
- [ ] Risks are reviewed

## Core Question

{project.core_question}

## Verified Claims


## Script Notes


## B-roll Plan


## Thumbnail Ideas


## Publishing Checklist


## Risks


"""
