import unittest
from datetime import datetime

from helpers import get_fixture_path

from src.backup_tools.backup_checker import IncorrectBackupConfig, load_config


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


if __name__ == "__main__":
    unittest.main()
