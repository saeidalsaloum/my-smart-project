import contextlib
import io
import subprocess
import sys
import unittest

from src.main import get_status_message, main

EXPECTED_STATUS = "my-smart-project: minimal Codex-ready starter is working."


class MainCliTest(unittest.TestCase):
    def test_status_message_function(self) -> None:
        self.assertEqual(get_status_message(), EXPECTED_STATUS)

    def test_main_returns_success_exit_code(self) -> None:
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), EXPECTED_STATUS)

    def test_cli_prints_status_message(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "src.main"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), EXPECTED_STATUS)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
