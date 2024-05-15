"""
Copyright 2024 Magic Pill Labs

DESCRIPTION:
    A simple ETL (Extract, Transform, Load) agent

INSTALL:
    pip install typer rich

USAGE EXAMPLE:
    > python datasmith.py chat --config your-config-path
    > python datasmith.py work --config your-config-path

LICENSE:
    All rights reserved.
"""


# ::IMPORTS ------------------------------------------------------------------------ #

# cli framework - https://pypi.org/project/typer/
import typer

# data types for validation - https://docs.python.org/3/library/typing.html
from typing import Optional
from typing import Optional
from typing_extensions import Annotated

# cross platform path handling - https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# Standard library import for package version retrieval - https://docs.python.org/3/library/importlib.metadata.html
from importlib.metadata import version

# Rich print for better formatting - https://rich.readthed.com/
from rich import print

# Project Imports
from pencilai import PencilAI



# ::SETUP -------------------------------------------------------------------------- #
cli = typer.Typer(
    add_completion=False, 
    no_args_is_help=True,
)

# ::SETUP SUBPARSERS --------------------------------------------------------------- #
# app.add_typer(<<module.app>>, name="subparser")

# ::GLOBALS --------------------------------------------------------------------- #
PKG_NAME = "pencilai"

# ::CORE LOGIC --------------------------------------------------------------------- #
# place core script logic here and call functions
# from the cli command functions to separate CLI from business logic

# ::CLI COMMANDS ---------------------------------------------------------------------------- #
@cli.command()
def chat(openai_api_key: str = "", base_dir: Optional[str] = "."):
    """ An interactive chat with the ETL agent """

    app = PencilAI(openai_api_key=openai_api_key, base_dir=base_dir)
    app.chat()
    



# ::DEFAULT CLI COMMANDS ---------------------------------------------------------------------------- #
@cli.command()
def version():
    """ get the version of the package """
    package_version = version(PKG_NAME)
    typer.echo(package_version)


# ::EXECUTE ------------------------------------------------------------------------ #
if __name__ == "__main__":  # ensure importing the script will not execute
    cli()
