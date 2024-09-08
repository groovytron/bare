import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest import TestCase

from click.testing import CliRunner
from freezegun import freeze_time

from src.backup_tools.backup_checker import LAST_FILE, load_config
from src.cli import COMMIT_MESSAGE, cli
from tests.helpers import get_fixture_path

mock_date = "2012-01-14 16:00:00"
mock_date_for_past = "2023-01-14 16:00:00"


class TestCliCommit(TestCase):
    def test_commit_no_config(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    def test_commit_empty_config(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("empty-last-backup")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    def test_commit_invalid_config(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("incorrect-config")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    def test_commit_invalid_timestamp(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("incorrect-timestamp")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    def test_commit_without_last_backup_key(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("without-last-backup-key")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    def test_commit_without_last_backup_interval_key(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = (
                Path(get_fixture_path("without-backup-interval-key"))
                / LAST_FILE
            )
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 1)

    @freeze_time(mock_date)
    def test_commit_after_init(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("after-init-config")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            before_config = load_config(str(test_path))
            before_date = before_config.last_backup_date
            before_interval = before_config.backup_interval

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 0)
            self.assertIn(COMMIT_MESSAGE, result.output)

            after_config = load_config(str(test_path))

            self.assertEqual(before_config.last_backup_date, before_date)
            self.assertEqual(before_config.backup_interval, before_interval)

            self.assertEqual(
                after_config.last_backup_date,
                datetime.fromisoformat(mock_date),
            )
            self.assertEqual(after_config.backup_interval, before_interval)

    @freeze_time(mock_date_for_past)
    def test_commit_backup_in_past(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("last-backup-in-past")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            before_config = load_config(str(test_path))
            before_date = before_config.last_backup_date
            before_interval = before_config.backup_interval

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 0)
            self.assertIn(COMMIT_MESSAGE, result.output)

            after_config = load_config(str(test_path))

            self.assertEqual(before_config.last_backup_date, before_date)
            self.assertEqual(before_config.backup_interval, before_interval)

            self.assertEqual(
                after_config.last_backup_date,
                datetime.fromisoformat(mock_date_for_past),
            )
            self.assertEqual(after_config.backup_interval, before_interval)

    @freeze_time(mock_date)
    def test_commit_backup_in_future(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("last-backup-in-future")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            before_config = load_config(str(test_path))
            before_date = before_config.last_backup_date
            before_interval = before_config.backup_interval

            os.environ["HOME"] = str(test_path)

            runner = CliRunner()
            result = runner.invoke(cli, ["commit"])

            self.assertEqual(result.exit_code, 0)
            self.assertNotIn(COMMIT_MESSAGE, result.output)

            after_config = load_config(str(test_path))

            self.assertEqual(before_config.last_backup_date, before_date)
            self.assertEqual(before_config.backup_interval, before_interval)

            self.assertEqual(
                after_config.last_backup_date,
                before_config.last_backup_date,
                "Backup should not be commited when \
                the last backup is in the future",
            )
            self.assertEqual(after_config.backup_interval, before_interval)
