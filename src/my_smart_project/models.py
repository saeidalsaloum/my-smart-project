"""Data model helpers for local content project records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from datetime import datetime, timedelta, timezone
import re
from typing import Any

PROJECT_NAME = "my-smart-project"
STATUS_MESSAGE = f"{PROJECT_NAME}: minimal Codex-ready starter is working."

ALLOWED_STATUSES = (
    "idea",
    "research",
    "script",
    "recording",
    "editing",
    "review",
    "scheduled",
    "published",
    "archived",
)
SECTION_STATUS_NOT_STARTED = "not_started"
SLUG_PATTERN = re.compile(r"^[a-z0-9_-]+$")


def get_status_message() -> str:
    """Return the deterministic project status message."""
    return STATUS_MESSAGE


def utc_now_iso() -> str:
    """Return the current UTC time in ISO 8601 format ending with Z."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def next_utc_iso_after(previous_timestamp: str) -> str:
    """Return a UTC timestamp that is later than the supplied timestamp."""
    current = utc_now_iso()
    if current != previous_timestamp:
        return current

    previous = datetime.fromisoformat(previous_timestamp.replace("Z", "+00:00"))
    return (previous + timedelta(microseconds=1)).isoformat().replace("+00:00", "Z")


def validate_slug(slug: str) -> str:
    """Validate and return a safe local filename slug."""
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "Slug must contain only lowercase letters, digits, hyphens, or underscores."
        )
    return slug


def validate_status(status: str) -> str:
    """Validate and return an allowed production status."""
    if status not in ALLOWED_STATUSES:
        allowed = ", ".join(ALLOWED_STATUSES)
        raise ValueError(f"Invalid status '{status}'. Allowed statuses: {allowed}.")
    return status


@dataclass
class VideoProject:
    """Safe local metadata for one video production project."""

    slug: str
    title: str
    status: str
    created_at: str
    updated_at: str
    core_question: str
    research_status: str
    script_status: str
    broll_status: str
    editing_status: str
    publishing_status: str
    notes: str

    @classmethod
    def create(cls, slug: str, title: str) -> "VideoProject":
        """Create a new project with safe default fields."""
        validate_slug(slug)
        if not title.strip():
            raise ValueError("Title must not be empty.")

        timestamp = utc_now_iso()
        return cls(
            slug=slug,
            title=title,
            status="idea",
            created_at=timestamp,
            updated_at=timestamp,
            core_question="",
            research_status=SECTION_STATUS_NOT_STARTED,
            script_status=SECTION_STATUS_NOT_STARTED,
            broll_status=SECTION_STATUS_NOT_STARTED,
            editing_status=SECTION_STATUS_NOT_STARTED,
            publishing_status=SECTION_STATUS_NOT_STARTED,
            notes="",
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VideoProject":
        """Load a project from a JSON object with the expected schema."""
        expected_fields = [field.name for field in fields(cls)]
        missing = [name for name in expected_fields if name not in data]
        extra = [name for name in data if name not in expected_fields]
        if missing or extra:
            details = []
            if missing:
                details.append(f"missing fields: {', '.join(missing)}")
            if extra:
                details.append(f"unexpected fields: {', '.join(extra)}")
            raise ValueError(f"Invalid project file schema ({'; '.join(details)}).")

        project = cls(**{name: data[name] for name in expected_fields})
        validate_slug(project.slug)
        validate_status(project.status)
        return project

    def to_dict(self) -> dict[str, str]:
        """Return the project as a JSON-serializable dictionary."""
        return asdict(self)
