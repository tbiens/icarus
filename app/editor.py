"""Function for the system text editor for changing settings."""

import click


def editor():
    """yes, this simple and it gets its own file."""
    click.edit(filename='./icarus.config')
