import tomllib
from unittest import TestCase

from click.testing import CliRunner

from backup_reminder.cli import cli


class TestCliVersion(TestCase):
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])

        self.assertEqual(result.exit_code, 0)

        with open("pyproject.toml", "rb") as project_file:
            config = tomllib.load(project_file)
            self.assertIn(
                f"bare version {config["tool"]["poetry"]["version"]}",
                result.output,
                "cli version should match pyproject.toml's version",
            )
