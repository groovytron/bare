import os
import tempfile
from pathlib import Path
from unittest import TestCase, mock

import yaml
from click.testing import CliRunner

from src.backup_tools.backup_checker import LAST_FILE
from src.cli import init

user_home = Path.home()


class TestCliConfigInit(TestCase):
    def test_init(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            os.environ["HOME"] = str(test_path)

            self.assertNotEqual(
                Path.home(),
                user_home,
                "HOME directory is not defined correctly for CLI testing",
            )

            runner = CliRunner()
            result = runner.invoke(init)

            self.assertEqual(result.exit_code, 0)

            with open(
                str(Path(str(test_path)) / LAST_FILE), "r"
            ) as config_file:
                config = yaml.safe_load(config_file.read())

                self.assertEqual(config["backup_interval"], 5)
                self.assertIsNone(config["last_backup"])

    def test_init_with_backup_interval_parameter(self):
        with tempfile.TemporaryDirectory(delete=False) as test_path:
            os.environ["HOME"] = str(test_path)

            self.assertNotEqual(
                Path.home(),
                user_home,
                "HOME directory is not defined correctly for CLI testing",
            )

            backup_interval = 12

            runner = CliRunner()
            result = runner.invoke(
                init, [f"--backup-interval={backup_interval}"]
            )

            self.assertEqual(result.exit_code, 0)

            with open(
                str(Path(str(test_path)) / LAST_FILE), "r"
            ) as config_file:
                config = yaml.safe_load(config_file.read())

                self.assertEqual(config["backup_interval"], backup_interval)
                self.assertIsNone(config["last_backup"])
