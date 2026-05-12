import json
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from src.main import get_status_message, main

EXPECTED_STATUS = "my-smart-project: minimal Codex-ready starter is working."
EXPECTED_FIELDS = [
    "slug",
    "title",
    "status",
    "created_at",
    "updated_at",
    "core_question",
    "research_status",
    "script_status",
    "broll_status",
    "editing_status",
    "publishing_status",
    "notes",
]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.main", *args],
        check=False,
        capture_output=True,
        text=True,
    )


class MainCliTest(unittest.TestCase):
    def test_status_message_function(self) -> None:
        self.assertEqual(get_status_message(), EXPECTED_STATUS)

    def test_main_returns_success_exit_code(self) -> None:
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main([])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), EXPECTED_STATUS)

    def test_cli_prints_status_message_without_command(self) -> None:
        result = run_cli()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), EXPECTED_STATUS)
        self.assertEqual(result.stderr, "")

    def test_status_command(self) -> None:
        result = run_cli("status")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), EXPECTED_STATUS)
        self.assertEqual(result.stderr, "")

    def test_help_command(self) -> None:
        result = run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)
        self.assertIn("status", result.stdout)
        self.assertIn("update-field", result.stdout)
        self.assertIn("update-section-status", result.stdout)
        self.assertIn("overview-videos", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_init_workspace_new_and_existing_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "content-workspace"

            first = run_cli("init-workspace", "--path", str(workspace))
            second = run_cli("init-workspace", "--path", str(workspace))

            self.assertEqual(first.returncode, 0)
            self.assertIn("Created content workspace:", first.stdout)
            self.assertEqual(second.returncode, 0)
            self.assertIn("Content workspace already exists:", second.stdout)
            self.assertTrue((workspace / "projects").is_dir())
            self.assertTrue((workspace / "exports").is_dir())
            self.assertTrue((workspace / "README.md").is_file())

    def test_init_workspace_refuses_existing_invalid_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            existing = Path(temp_dir) / "existing"
            existing.mkdir()

            result = run_cli("init-workspace", "--path", str(existing))

            self.assertEqual(result.returncode, 1)
            self.assertIn("not a valid content workspace", result.stderr)

    def test_new_video_creation_and_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            result = run_cli(
                "new-video",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--title",
                "First Video",
            )

            project_path = workspace / "projects" / "first-video.json"
            data = json.loads(project_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(list(data.keys()), EXPECTED_FIELDS)
            self.assertEqual(data["slug"], "first-video")
            self.assertEqual(data["title"], "First Video")
            self.assertEqual(data["status"], "idea")
            self.assertEqual(data["created_at"], data["updated_at"])
            self.assertTrue(data["created_at"].endswith("Z"))
            self.assertEqual(data["research_status"], "not_started")
            self.assertEqual(data["script_status"], "not_started")
            self.assertEqual(data["broll_status"], "not_started")
            self.assertEqual(data["editing_status"], "not_started")
            self.assertEqual(data["publishing_status"], "not_started")
            self.assertEqual(data["core_question"], "")
            self.assertEqual(data["notes"], "")

    def test_new_video_refuses_duplicate_slug(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")

            result = run_cli(
                "new-video",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--title",
                "Duplicate",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("already exists", result.stderr)

    def test_list_videos_empty_and_sorted_projects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            empty = run_cli("list-videos", "--workspace", str(workspace))
            self._new_video(workspace, "z-video", "Z Video")
            self._new_video(workspace, "a-video", "A Video")
            listed = run_cli("list-videos", "--workspace", str(workspace))

            self.assertEqual(empty.returncode, 0)
            self.assertIn("No video projects found.", empty.stdout)
            self.assertEqual(listed.returncode, 0)
            self.assertIn("SLUG", listed.stdout)
            self.assertNotIn("RESEARCH", listed.stdout)
            self.assertLess(listed.stdout.index("a-video"), listed.stdout.index("z-video"))

    def test_overview_videos_empty_and_section_status_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            empty = run_cli("overview-videos", "--workspace", str(workspace))
            self._new_video(workspace, "z-video", "Z Video")
            self._new_video(workspace, "a-video", "A Video")
            status_update = run_cli(
                "update-status",
                "--workspace",
                str(workspace),
                "--slug",
                "z-video",
                "--status",
                "editing",
            )
            self.assertEqual(status_update.returncode, 0, status_update.stderr)
            updates = [
                ("a-video", "research", "in_progress"),
                ("a-video", "script", "done"),
                ("z-video", "broll", "blocked"),
                ("z-video", "editing", "in_progress"),
                ("z-video", "publishing", "done"),
            ]
            for slug, section, status in updates:
                result = run_cli(
                    "update-section-status",
                    "--workspace",
                    str(workspace),
                    "--slug",
                    slug,
                    "--section",
                    section,
                    "--status",
                    status,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            overview = run_cli("overview-videos", "--workspace", str(workspace))
            filtered = run_cli(
                "overview-videos",
                "--workspace",
                str(workspace),
                "--status",
                "editing",
            )

            self.assertEqual(empty.returncode, 0)
            self.assertIn("No video projects found.", empty.stdout)
            self.assertEqual(overview.returncode, 0, overview.stderr)
            self.assertEqual(filtered.returncode, 0, filtered.stderr)
            lines = overview.stdout.splitlines()
            self.assertEqual(
                lines[0].split(maxsplit=7),
                [
                    "SLUG",
                    "STATUS",
                    "RESEARCH",
                    "SCRIPT",
                    "B-ROLL",
                    "EDITING",
                    "PUBLISHING",
                    "TITLE",
                ],
            )
            self.assertLess(
                overview.stdout.index("a-video"),
                overview.stdout.index("z-video"),
            )
            a_video_row = next(line for line in lines if line.startswith("a-video"))
            z_video_row = next(line for line in lines if line.startswith("z-video"))
            self.assertEqual(
                a_video_row.split(maxsplit=7),
                [
                    "a-video",
                    "idea",
                    "in_progress",
                    "done",
                    "not_started",
                    "not_started",
                    "not_started",
                    "A Video",
                ],
            )
            self.assertEqual(
                z_video_row.split(maxsplit=7),
                [
                    "z-video",
                    "editing",
                    "not_started",
                    "not_started",
                    "blocked",
                    "in_progress",
                    "done",
                    "Z Video",
                ],
            )
            self.assertIn("z-video", filtered.stdout)
            self.assertIn("editing", filtered.stdout)
            self.assertIn("Z Video", filtered.stdout)
            self.assertNotIn("a-video", filtered.stdout)
            self.assertNotIn("A Video", filtered.stdout)

    def test_overview_videos_rejects_invalid_status_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            result = run_cli(
                "overview-videos",
                "--workspace",
                str(workspace),
                "--status",
                "blocked",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid choice", result.stderr)

    def test_show_video_prints_project_detail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")

            result = run_cli(
                "show-video",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Title: First Video", result.stdout)
            self.assertIn("Slug: first-video", result.stdout)
            self.assertIn("Status: idea", result.stdout)
            self.assertIn("Research Status: not_started", result.stdout)

    def test_update_status_changes_status_and_updated_at(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = json.loads(project_path.read_text(encoding="utf-8"))

            result = run_cli(
                "update-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--status",
                "editing",
            )

            after = json.loads(project_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(after["status"], "editing")
            self.assertEqual(after["created_at"], before["created_at"])
            self.assertNotEqual(after["updated_at"], before["updated_at"])

    def test_update_status_rejects_invalid_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")

            result = run_cli(
                "update-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--status",
                "blocked",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid choice", result.stderr)

    def test_update_field_updates_core_question_preserves_schema_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = json.loads(project_path.read_text(encoding="utf-8"))

            result = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--field",
                "core_question",
                "--value",
                "Why does this topic matter?",
            )

            after = json.loads(project_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "Updated first-video core_question.")
            self.assertEqual(list(after.keys()), EXPECTED_FIELDS)
            self.assertEqual(after["core_question"], "Why does this topic matter?")
            self.assertEqual(after["notes"], before["notes"])
            self.assertNotEqual(after["updated_at"], before["updated_at"])
            self.assertEqual(after["created_at"], before["created_at"])
            self.assertEqual(after["slug"], before["slug"])
            self.assertEqual(after["title"], before["title"])
            self.assertEqual(after["status"], before["status"])
            self.assertEqual(after["research_status"], before["research_status"])
            self.assertEqual(after["script_status"], before["script_status"])
            self.assertEqual(after["broll_status"], before["broll_status"])
            self.assertEqual(after["editing_status"], before["editing_status"])
            self.assertEqual(after["publishing_status"], before["publishing_status"])

    def test_update_field_updates_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = json.loads(project_path.read_text(encoding="utf-8"))

            result = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--field",
                "notes",
                "--value",
                "Draft notes here.",
            )

            after = json.loads(project_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(after["notes"], "Draft notes here.")
            self.assertEqual(after["core_question"], before["core_question"])
            self.assertNotEqual(after["updated_at"], before["updated_at"])
            self.assertEqual(after["created_at"], before["created_at"])

    def test_update_field_rejects_unsupported_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = project_path.read_text(encoding="utf-8")

            result = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--field",
                "title",
                "--value",
                "Unsafe Title Update",
            )

            after = project_path.read_text(encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Unsupported project field 'title'", result.stderr)
            self.assertEqual(after, before)

    def test_update_field_rejects_missing_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            result = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "missing-video",
                "--field",
                "notes",
                "--value",
                "Draft notes here.",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Video project not found: missing-video", result.stderr)

    def test_update_field_writes_only_target_project_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            self._new_video(workspace, "second-video", "Second Video")
            export = run_cli(
                "export-brief",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
            )
            self.assertEqual(export.returncode, 0, export.stderr)
            before_files = self._workspace_file_snapshots(workspace)

            result = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--field",
                "notes",
                "--value",
                "Draft notes here.",
            )

            after_files = self._workspace_file_snapshots(workspace)
            changed_files = [
                name for name in before_files if before_files[name] != after_files[name]
            ]
            self.assertEqual(result.returncode, 0)
            self.assertEqual(sorted(after_files), sorted(before_files))
            self.assertEqual(changed_files, ["projects/first-video.json"])

    def test_update_section_status_updates_each_section_preserves_schema_and_metadata(
        self,
    ) -> None:
        section_cases = [
            ("research", "research_status", "in_progress"),
            ("script", "script_status", "done"),
            ("broll", "broll_status", "blocked"),
            ("editing", "editing_status", "in_progress"),
            ("publishing", "publishing_status", "done"),
        ]

        for section, field_name, status in section_cases:
            with self.subTest(section=section):
                with tempfile.TemporaryDirectory() as temp_dir:
                    workspace = self._init_workspace(temp_dir)
                    self._new_video(workspace, "first-video", "First Video")
                    core_question = run_cli(
                        "update-field",
                        "--workspace",
                        str(workspace),
                        "--slug",
                        "first-video",
                        "--field",
                        "core_question",
                        "--value",
                        "Why does this topic matter?",
                    )
                    notes = run_cli(
                        "update-field",
                        "--workspace",
                        str(workspace),
                        "--slug",
                        "first-video",
                        "--field",
                        "notes",
                        "--value",
                        "Draft notes here.",
                    )
                    self.assertEqual(core_question.returncode, 0, core_question.stderr)
                    self.assertEqual(notes.returncode, 0, notes.stderr)
                    project_path = workspace / "projects" / "first-video.json"
                    before = json.loads(project_path.read_text(encoding="utf-8"))

                    result = run_cli(
                        "update-section-status",
                        "--workspace",
                        str(workspace),
                        "--slug",
                        "first-video",
                        "--section",
                        section,
                        "--status",
                        status,
                    )

                    after = json.loads(project_path.read_text(encoding="utf-8"))
                    self.assertEqual(result.returncode, 0)
                    self.assertEqual(
                        result.stdout.strip(),
                        f"Updated first-video {section} status to {status}.",
                    )
                    self.assertEqual(list(after.keys()), EXPECTED_FIELDS)
                    self.assertEqual(after[field_name], status)
                    self.assertNotEqual(after["updated_at"], before["updated_at"])
                    self.assertEqual(after["created_at"], before["created_at"])
                    self.assertEqual(after["slug"], before["slug"])
                    self.assertEqual(after["title"], before["title"])
                    self.assertEqual(after["status"], before["status"])
                    self.assertEqual(after["core_question"], before["core_question"])
                    self.assertEqual(after["notes"], before["notes"])
                    for other_section, other_field_name, _ in section_cases:
                        if other_section != section:
                            self.assertEqual(
                                after[other_field_name], before[other_field_name]
                            )

    def test_update_section_status_rejects_unsupported_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = project_path.read_text(encoding="utf-8")

            result = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "thumbnail",
                "--status",
                "in_progress",
            )

            after = project_path.read_text(encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Unsupported project section 'thumbnail'", result.stderr)
            self.assertEqual(after, before)

    def test_update_section_status_rejects_unsupported_status_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            before = project_path.read_text(encoding="utf-8")

            result = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "reviewing",
            )

            after = project_path.read_text(encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Unsupported section status 'reviewing'", result.stderr)
            self.assertEqual(after, before)

    def test_update_section_status_rejects_missing_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            result = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "missing-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Video project not found: missing-video", result.stderr)

    def test_update_section_status_repeated_same_status_bumps_updated_at(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"

            first = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )
            before_repeat_text = project_path.read_text(encoding="utf-8")
            before_repeat = json.loads(before_repeat_text)

            second = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )

            after_repeat_text = project_path.read_text(encoding="utf-8")
            after_repeat = json.loads(after_repeat_text)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(after_repeat["research_status"], "in_progress")
            self.assertNotEqual(after_repeat_text, before_repeat_text)
            self.assertNotEqual(
                after_repeat["updated_at"], before_repeat["updated_at"]
            )
            for field_name in EXPECTED_FIELDS:
                if field_name != "updated_at":
                    self.assertEqual(after_repeat[field_name], before_repeat[field_name])

    def test_update_section_status_can_return_section_to_not_started(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"

            first = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )
            before_return = json.loads(project_path.read_text(encoding="utf-8"))

            second = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "not_started",
            )

            after_return = json.loads(project_path.read_text(encoding="utf-8"))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(after_return["research_status"], "not_started")
            self.assertNotEqual(after_return["updated_at"], before_return["updated_at"])
            self.assertEqual(after_return["created_at"], before_return["created_at"])
            self.assertEqual(after_return["slug"], before_return["slug"])
            self.assertEqual(after_return["title"], before_return["title"])
            self.assertEqual(after_return["status"], before_return["status"])

    def test_show_video_rejects_corrupted_stored_section_statuses(self) -> None:
        section_status_fields = [
            "research_status",
            "script_status",
            "broll_status",
            "editing_status",
            "publishing_status",
        ]

        for field_name in section_status_fields:
            with self.subTest(field_name=field_name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    workspace = self._init_workspace(temp_dir)
                    self._new_video(workspace, "first-video", "First Video")
                    project_path = workspace / "projects" / "first-video.json"
                    data = json.loads(project_path.read_text(encoding="utf-8"))
                    data[field_name] = "reviewing"
                    corrupted = json.dumps(data, indent=2) + "\n"
                    project_path.write_text(corrupted, encoding="utf-8")

                    result = run_cli(
                        "show-video",
                        "--workspace",
                        str(workspace),
                        "--slug",
                        "first-video",
                    )

                    after = project_path.read_text(encoding="utf-8")
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("Invalid project file", result.stderr)
                    self.assertIn(
                        f"Invalid section status 'reviewing' for {field_name}",
                        result.stderr,
                    )
                    self.assertEqual(after, corrupted)

    def test_update_section_status_rejects_corrupted_stored_status_before_write(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            data = json.loads(project_path.read_text(encoding="utf-8"))
            data["script_status"] = "reviewing"
            corrupted = json.dumps(data, indent=2) + "\n"
            project_path.write_text(corrupted, encoding="utf-8")

            result = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )

            after = project_path.read_text(encoding="utf-8")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Invalid project file", result.stderr)
            self.assertIn(
                "Invalid section status 'reviewing' for script_status",
                result.stderr,
            )
            self.assertEqual(after, corrupted)

    def test_show_video_loads_stored_projects_with_allowed_section_statuses(
        self,
    ) -> None:
        allowed_statuses = ["not_started", "in_progress", "blocked", "done"]
        section_status_fields = [
            "research_status",
            "script_status",
            "broll_status",
            "editing_status",
            "publishing_status",
        ]

        for status in allowed_statuses:
            with self.subTest(status=status):
                with tempfile.TemporaryDirectory() as temp_dir:
                    workspace = self._init_workspace(temp_dir)
                    self._new_video(workspace, "first-video", "First Video")
                    project_path = workspace / "projects" / "first-video.json"
                    data = json.loads(project_path.read_text(encoding="utf-8"))
                    for field_name in section_status_fields:
                        data[field_name] = status
                    project_path.write_text(
                        json.dumps(data, indent=2) + "\n",
                        encoding="utf-8",
                    )

                    result = run_cli(
                        "show-video",
                        "--workspace",
                        str(workspace),
                        "--slug",
                        "first-video",
                    )

                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(f"Research Status: {status}", result.stdout)
                    self.assertIn(f"Script Status: {status}", result.stdout)
                    self.assertIn(f"B-roll Status: {status}", result.stdout)
                    self.assertIn(f"Editing Status: {status}", result.stdout)
                    self.assertIn(f"Publishing Status: {status}", result.stdout)

    def test_update_section_status_writes_only_target_project_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            self._new_video(workspace, "second-video", "Second Video")
            export = run_cli(
                "export-brief",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
            )
            self.assertEqual(export.returncode, 0, export.stderr)
            before_files = self._workspace_file_snapshots(workspace)

            result = run_cli(
                "update-section-status",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--section",
                "research",
                "--status",
                "in_progress",
            )

            after_files = self._workspace_file_snapshots(workspace)
            changed_files = [
                name for name in before_files if before_files[name] != after_files[name]
            ]
            self.assertEqual(result.returncode, 0)
            self.assertEqual(sorted(after_files), sorted(before_files))
            self.assertEqual(changed_files, ["projects/first-video.json"])

    def test_missing_project_handling(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)

            result = run_cli(
                "show-video",
                "--workspace",
                str(workspace),
                "--slug",
                "missing-video",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("Video project not found: missing-video", result.stderr)

    def test_export_brief_and_refuse_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")

            first = run_cli("export-brief", "--workspace", str(workspace), "--slug", "first-video")
            second = run_cli("export-brief", "--workspace", str(workspace), "--slug", "first-video")

            brief_path = workspace / "exports" / "first-video_brief.md"
            brief = brief_path.read_text(encoding="utf-8")
            self.assertEqual(first.returncode, 0)
            self.assertTrue(brief_path.is_file())
            self.assertIn("# First Video", brief)
            self.assertIn("## Project Metadata", brief)
            self.assertIn("## Section Statuses", brief)
            self.assertIn("- Slug: `first-video`", brief)
            self.assertIn("- Production Status: `idea`", brief)
            self.assertIn("## Core Question", brief)
            self.assertIn("## Verified Claims", brief)
            self.assertIn("## Script Notes", brief)
            self.assertIn("## B-roll Plan", brief)
            self.assertIn("## Thumbnail Ideas", brief)
            self.assertIn("## Publishing Checklist", brief)
            self.assertIn("## Risks", brief)
            self.assertEqual(second.returncode, 1)
            self.assertIn("Brief already exists", second.stderr)

    def test_export_brief_includes_safe_metadata_and_current_section_statuses(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = self._init_workspace(temp_dir)
            self._new_video(workspace, "first-video", "First Video")
            project_path = workspace / "projects" / "first-video.json"
            updates = [
                ("research", "in_progress", "- Research: `in_progress`"),
                ("script", "done", "- Script: `done`"),
                ("broll", "blocked", "- B-roll: `blocked`"),
                ("editing", "in_progress", "- Editing: `in_progress`"),
                ("publishing", "done", "- Publishing: `done`"),
            ]
            notes = run_cli(
                "update-field",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
                "--field",
                "notes",
                "--value",
                "Draft notes should stay private.",
            )
            self.assertEqual(notes.returncode, 0, notes.stderr)
            for section, status, _ in updates:
                result = run_cli(
                    "update-section-status",
                    "--workspace",
                    str(workspace),
                    "--slug",
                    "first-video",
                    "--section",
                    section,
                    "--status",
                    status,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(project_path.read_text(encoding="utf-8"))

            export = run_cli(
                "export-brief",
                "--workspace",
                str(workspace),
                "--slug",
                "first-video",
            )

            brief = (workspace / "exports" / "first-video_brief.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(export.returncode, 0, export.stderr)
            self.assertIn("## Project Metadata", brief)
            self.assertIn("- Slug: `first-video`", brief)
            self.assertIn("- Production Status: `idea`", brief)
            self.assertIn(f"- Created At: `{data['created_at']}`", brief)
            self.assertIn(f"- Updated At: `{data['updated_at']}`", brief)
            self.assertIn("## Section Statuses", brief)
            for _, _, expected_line in updates:
                self.assertIn(expected_line, brief)
            self.assertLess(
                brief.index("## Project Metadata"),
                brief.index("## Section Statuses"),
            )
            self.assertLess(
                brief.index("## Section Statuses"),
                brief.index("## Production Checklist"),
            )
            self.assertNotIn("Draft notes should stay private.", brief)
            self.assertNotIn("## Notes", brief)

    def _init_workspace(self, temp_dir: str) -> Path:
        workspace = Path(temp_dir) / "content-workspace"
        result = run_cli("init-workspace", "--path", str(workspace))
        self.assertEqual(result.returncode, 0, result.stderr)
        return workspace

    def _new_video(self, workspace: Path, slug: str, title: str) -> None:
        result = run_cli(
            "new-video",
            "--workspace",
            str(workspace),
            "--slug",
            slug,
            "--title",
            title,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def _workspace_file_snapshots(self, workspace: Path) -> dict[str, str]:
        return {
            str(path.relative_to(workspace)): path.read_text(encoding="utf-8")
            for path in sorted(workspace.rglob("*"))
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
