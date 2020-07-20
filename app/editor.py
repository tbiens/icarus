import click


def editor():
    message = click.edit(filename='./icarus.config')
