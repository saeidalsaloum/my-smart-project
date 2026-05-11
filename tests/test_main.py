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
            self.assertLess(listed.stdout.index("a-video"), listed.stdout.index("z-video"))

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
            self.assertIn("## Core Question", brief)
            self.assertIn("## Verified Claims", brief)
            self.assertIn("## Script Notes", brief)
            self.assertIn("## B-roll Plan", brief)
            self.assertIn("## Thumbnail Ideas", brief)
            self.assertIn("## Publishing Checklist", brief)
            self.assertIn("## Risks", brief)
            self.assertEqual(second.returncode, 1)
            self.assertIn("Brief already exists", second.stderr)

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


if __name__ == "__main__":
    unittest.main()
