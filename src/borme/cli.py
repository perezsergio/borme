from io import TextIOWrapper
from typing import Callable

import click
from logs import (
    log_dates_from_cl_and_file,
    set_up_root_logger,
)
from utils.cli_help_message import construct_help_message


def dates_cli(func_of_dates: Callable[[tuple[str, ...]], None]) -> click.Command:
    """Add cli functionality to a function that accepts a list of dates as argument."""
    set_up_root_logger()

    class CmdWithCustomHelpMessage(click.Command):
        """
        Creates a click.Group class and override format_help method.
        This is the easiest way to get a custom --help message with click.
        """

        def format_help(self, ctx, formatter):
            click.echo(construct_help_message(func_of_dates))

    @click.command(cls=CmdWithCustomHelpMessage)
    @click.argument("input_dates", nargs=-1, type=str)
    @click.option(
        "-f",
        "--file",
        type=click.File("r"),
    )
    def func_of_dates_with_cli(input_dates: tuple[str, ...], file: TextIOWrapper):
        # Cannot pass dates from both the command line and a text file
        if file is not None and len(input_dates) != 0:
            log_dates_from_cl_and_file()

        if file is not None:
            # if a file was passed to the cli, get dates from file
            contents = file.read()
            input_dates = tuple(contents.splitlines())

        func_of_dates(input_dates)

    return func_of_dates_with_cli
