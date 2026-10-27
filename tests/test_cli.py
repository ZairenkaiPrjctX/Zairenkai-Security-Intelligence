import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from zsi import cli


class ScanCommandTest(unittest.TestCase):
    def test_scan_of_current_directory_records_nonempty_repository_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.json"
            result = subprocess.CompletedProcess(
                args=["osv-scanner"], returncode=0, stdout='{"results": []}', stderr=""
            )
            argv = ["zsi", "scan", "--repository", ".", "--commit", "abc123", "--output", str(output)]
            with (
                patch.object(sys, "argv", argv),
                patch("zsi.cli.shutil.which", return_value="/usr/bin/osv-scanner"),
                patch("zsi.cli.subprocess.run", return_value=result),
            ):
                self.assertEqual(cli.main(), 0)

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["repository"], Path.cwd().name)
            self.assertTrue(report["repository"])


if __name__ == "__main__":
    unittest.main()
