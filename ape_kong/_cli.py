import click

from ape import config
from .game import play


@click.command(short_help="Play Ape Kong")
def kong():
    piece = config.get_config("kong").piece
    play(piece)
