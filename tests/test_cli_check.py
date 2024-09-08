import os
import re
from unittest import TestCase

from click.testing import CliRunner

from src.cli import (
    BACKUP_NEVER_PERFORMED_MESSAGE,
    CONFIG_ERROR_MESSAGE,
    NO_BACKUP_NEEDED_MESSAGE,
    NO_CONFIG_MESSAGE,
    cli,
)
from tests.helpers import get_fixture_path


class TestCliCheck(TestCase):
    def test_no_config(self):
        test_path = get_fixture_path("no-backup")

        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn(NO_CONFIG_MESSAGE, result.output)

    def test_empty_config(self):
        test_path = get_fixture_path("empty-last-backup")

        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn(CONFIG_ERROR_MESSAGE, result.output)

    def test_invalid_config(self):
        test_path = get_fixture_path("incorrect-config")

        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn(CONFIG_ERROR_MESSAGE, result.output)

    def test_config_without_last_backup(self):
        test_path = get_fixture_path("without-last-backup-key")

        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn(CONFIG_ERROR_MESSAGE, result.output)

    def test_config_without_backup_interval(self):
        test_path = get_fixture_path("without-backup-interval-key")

        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn(CONFIG_ERROR_MESSAGE, result.output)

    def test_last_backup_never_done(self):
        test_path = get_fixture_path("after-init-config")
        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(BACKUP_NEVER_PERFORMED_MESSAGE, result.output)

    def test_last_backup_in_past(self):
        test_path = get_fixture_path("last-backup-in-past")
        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 0)
        self.assertIsNotNone(
            re.match(r"Your last backup was done \d+ days ago", result.output)
        )

    def test_last_backup_in_future(self):
        test_path = get_fixture_path("last-backup-in-future")
        os.environ["HOME"] = str(test_path)

        runner = CliRunner()
        result = runner.invoke(cli, ["check"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(NO_BACKUP_NEEDED_MESSAGE, result.output)
