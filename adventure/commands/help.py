"""Display the available commands to the player in the game."""

from adventure.game import Game
from adventure.commands.command import Command
from .command_response import CommandResponse


def help_cmd(game: Game, *args, **kwargs) -> CommandResponse:
    """Display the available commands."""
    response = CommandResponse()
    response.add_message("Available commands:", "green")
    for cmd in game.interpreter.commands:
        if isinstance(cmd, Command):
            response.add_message(f"{cmd.name}: {cmd.help_text}", "blue")
    response.add_message(
        "Type 'help <command>' for more information on a specific command.", "green"
    )
    return response
