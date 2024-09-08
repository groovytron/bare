from pathlib import Path
from notifypy import Notify

import click

from src.backup_tools.backup_checker import (
    IncorrectBackupConfig,
    commit_backup,
    compute_last_backup_age_in_days,
    load_config,
    new_backup_is_needed,
)
from src.generator.generator import init_config

notification = Notify(
  default_notification_title="Backups status",
  default_application_name="Backup Checker",
)

BACKUP_NEVER_PERFORMED_MESSAGE = "You have never performed a backup. " \
    "Please make one as soon as possible."

NO_BACKUP_NEEDED_MESSAGE = "No backup needed you're all good and safe."

NO_CONFIG_MESSAGE = "No configuration file found. " \
    "Please create one with the init command."

CONFIG_ERROR_MESSAGE = "An error occured during configuration loading. " \
    "Please check and fix your configuration file."


@click.group()
def cli():
    pass


@cli.command(help="Initialize the backup checker configuration.")
@click.option(
    "--backup-interval",
    default=5,
    help="""Amount of days between backups. A notification will be sent after
    this amount of days passed without any backup.""",
)
def init(backup_interval):
    click.echo("Generating configuration...")
    config_file = init_config(Path.home(), backup_interval)
    click.echo(f"Configuration generated in {config_file}")


@cli.command(help="Check if a new backup is necessary.")
def check():
    try:
        config = load_config(Path.home())
        backup_is_needed = new_backup_is_needed(config)

        if backup_is_needed:
            age = compute_last_backup_age_in_days(config)

            if age is None:
                message = BACKUP_NEVER_PERFORMED_MESSAGE
                click.echo(message)

                notification.message = message
                notification.title = "You need a new backup"
                notification.send()

                return

            message = f"Your last backup was done {age} days ago. " \
                "Please make a new one as soon as possible."
            click.echo(message)

            notification.message = message
            notification.title = "You need a new backup"
            notification.send()

            return

        click.echo(NO_BACKUP_NEEDED_MESSAGE)
    except IncorrectBackupConfig:
        click.echo(CONFIG_ERROR_MESSAGE)
        exit(1)
    except FileNotFoundError:
        click.echo(NO_CONFIG_MESSAGE)
        exit(1)


@cli.command(help="Commit your backup.")
def commit():
    try:
        config = load_config(Path.home())

        if new_backup_is_needed(config):
            commit_backup(Path.home())
    except IncorrectBackupConfig:
        click.echo(CONFIG_ERROR_MESSAGE)
        exit(1)
    except FileNotFoundError:
        click.echo(NO_CONFIG_MESSAGE)
        exit(1)


if __name__ == "__main__":
    cli()
