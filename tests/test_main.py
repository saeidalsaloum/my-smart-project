import subprocess
import sys
import unittest

from src.main import get_status_message


class MainCliTest(unittest.TestCase):
    def test_status_message_function(self) -> None:
        self.assertEqual(
            get_status_message(),
            "my-smart-project: minimal Codex-ready starter is working.",
        )

    def test_cli_prints_status_message(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "src.main"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            result.stdout.strip(),
            "my-smart-project: minimal Codex-ready starter is working.",
        )


if __name__ == "__main__":
    unittest.main()
