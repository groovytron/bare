import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest import TestCase

from freezegun import freeze_time

from src.backup_tools.backup_checker import (
    LAST_FILE,
    commit_backup,
    load_config,
)
from tests.helpers import get_fixture_path

mock_date = "2012-01-14 16:00:00"


class TestUpdateConfig(TestCase):
    @freeze_time(mock_date)
    def test_commit_after_init(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            src = Path(get_fixture_path("after-init-config")) / LAST_FILE
            dest = Path(str(test_path)) / LAST_FILE

            shutil.copy(src, dest)

            before_config = load_config(str(test_path))
            before_date = before_config.last_backup_date
            before_interval = before_config.backup_interval

            commit_backup(test_path)

            after_config = load_config(str(test_path))

            self.assertEqual(before_config.last_backup_date, before_date)
            self.assertEqual(before_config.backup_interval, before_interval)

            self.assertEqual(
                after_config.last_backup_date,
                datetime.fromisoformat(mock_date),
            )
            self.assertEqual(after_config.backup_interval, before_interval)
