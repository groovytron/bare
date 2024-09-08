from pathlib import Path

import click

from src.backup_tools.backup_checker import (
    IncorrectBackupConfig,
    compute_last_backup_age_in_days,
    load_config,
    new_backup_is_needed,
)
from src.generator.generator import init_config


@click.group()
def cli():
    pass


@cli.command(help="Initialize the backup checker configuration")
@click.option(
    "--backup-interval",
    default=5,
    help="""Amount of days between backups. A notification will be sent after
    this amount of days passed without any backup""",
)
def init(backup_interval):
    click.echo("Generating configuration...")
    config_file = init_config(Path.home(), backup_interval)
    click.echo(f"Configuration generated in {config_file}")


@cli.command(help="Check if a new backup is necessary")
def check():
    try:
        config = load_config(Path.home())
        backup_is_needed = new_backup_is_needed(config)

        if backup_is_needed:
            age = compute_last_backup_age_in_days(config)

            if age is None:
                click.echo(
                    """You have never performed a backup.
                           Please make one as soon as possible."""
                )
                return

            click.echo(
                f"""Your last backup was done {age} days ago.
                       Please make a new one as soon as possible."""
            )
            return

        click.echo("No backup needed you're all good and safe.")
    except IncorrectBackupConfig:
        click.echo(
            """An error occured during configuration loading.
            Please check and fix your configuration file."""
        )


if __name__ == "__main__":
    cli()
