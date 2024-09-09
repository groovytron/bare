import re
from unittest import TestCase

from click.testing import CliRunner

from backup_reminder.cli import cli


class TestCliVersion(TestCase):
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])

        self.assertEqual(result.exit_code, 0)
        self.assertIsNotNone(
            re.match(r"bare version \d+.\d+.\d+", result.output)
        )
