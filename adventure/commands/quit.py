"""Quit the game command."""

from adventure.game import Game
from .command_response import CommandResponse


def quit_game(game: Game, *args, **kwargs) -> CommandResponse:
    """We are LEAVING!"""
    game.is_running = False
    return CommandResponse("Goodbye!", "yellow")
