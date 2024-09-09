import unittest
from datetime import datetime

from helpers import get_fixture_path

from backup_reminder.checker import IncorrectBackupConfig, load_config


class TestLoadConfig(unittest.TestCase):
    def test_no_config(self):
        test_path = get_fixture_path("no-backup")

        with self.assertRaises(FileNotFoundError):
            load_config(test_path)

    def test_empty_config(self):
        test_path = get_fixture_path("empty-last-backup")

        with self.assertRaises(IncorrectBackupConfig):
            load_config(test_path)

    def test_invalid_config(self):
        test_path = get_fixture_path("incorrect-config")

        with self.assertRaises(IncorrectBackupConfig):
            load_config(test_path)

    def test_config_without_last_backup(self):
        test_path = get_fixture_path("without-last-backup-key")

        with self.assertRaises(IncorrectBackupConfig):
            load_config(test_path)

    def test_config_without_backup_interval(self):
        test_path = get_fixture_path("without-backup-interval-key")

        with self.assertRaises(IncorrectBackupConfig):
            load_config(test_path)

    def test_after_init_config(self):
        test_path = get_fixture_path("after-init-config")

        config = load_config(test_path)

        self.assertIsNone(config.last_backup_date)
        self.assertEqual(config.backup_interval, 5)

    def test_last_backup_in_past(self):
        test_path = get_fixture_path("last-backup-in-past")

        config = load_config(test_path)

        self.assertEqual(
            config.last_backup_date, datetime.fromtimestamp(1662475201)
        )
        self.assertEqual(config.backup_interval, 5)

    def test_last_backup_in_future(self):
        test_path = get_fixture_path("last-backup-in-future")

        config = load_config(test_path)

        self.assertEqual(
            config.last_backup_date, datetime.fromtimestamp(33282542401)
        )
        self.assertEqual(config.backup_interval, 5)


if __name__ == "__main__":
    unittest.main()
