from pathlib import Path

import click

from src.generator.generator import init_config


@click.command()
@click.option(
    "--backup-interval",
    default=5,
    help="""Amount of days between backups. A notification will be sent after
    this amount of days passed without any backup""",
)
def init(backup_interval):
    config_file = init_config(Path.home(), backup_interval)
    click.echo(f"Configuration generated in {config_file}")


if __name__ == "__main__":
    init()
