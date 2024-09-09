import tempfile
import unittest
from pathlib import Path

from helpers import get_fixture_path

from backup_reminder.checker import LAST_FILE
from backup_reminder.generator import init_config


class TestGeneratorConfigInit(unittest.TestCase):
    def test_init(self):
        with tempfile.TemporaryDirectory() as test_path:
            config_file_path = init_config(str(test_path))

            with open(config_file_path, "r") as config_file:
                with open(
                    Path(get_fixture_path("after-init-config") / LAST_FILE)
                ) as result_file:
                    self.assertEqual(config_file.read(), result_file.read())
