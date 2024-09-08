import unittest

from helpers import get_fixture_path

from src.backup_tools.backup_checker import (
    IncorrectBackupConfig,
    config_file_exists,
    load_config,
)


class TestLoadConfig(unittest.TestCase):
    def test_no_last_backup(self):
        test_path = get_fixture_path("no-backup")

        self.assertFalse(config_file_exists(str(test_path)))

    def test_empty_last_backup(self):
        test_path = get_fixture_path("empty-last-backup")

        self.assertTrue(config_file_exists(str(test_path)))

    def test_last_backup_in_past(self):
        test_path = get_fixture_path("last-backup-in-past")

        self.assertTrue(config_file_exists(str(test_path)))

    def test_last_backup_in_future(self):
        test_path = get_fixture_path("last-backup-in-future")

        self.assertTrue(config_file_exists(str(test_path)))

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


if __name__ == "__main__":
    unittest.main()
