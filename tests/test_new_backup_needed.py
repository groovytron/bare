import unittest

from helpers import get_fixture_path

from src.backup_tools.backup_checker import load_config, new_backup_is_needed


class TestNewBackupNeeded(unittest.TestCase):
    def test_last_backup_never_done(self):
        test_path = get_fixture_path("after-init-config")
        config = load_config(test_path)

        self.assertTrue(new_backup_is_needed(config))

    def test_last_backup_in_past(self):
        test_path = get_fixture_path("last-backup-in-past")
        config = load_config(test_path)

        self.assertTrue(new_backup_is_needed(config))

    def test_last_backup_in_future(self):
        test_path = get_fixture_path("last-backup-in-future")
        config = load_config(test_path)

        self.assertFalse(new_backup_is_needed(config))


if __name__ == "__main__":
    unittest.main()
