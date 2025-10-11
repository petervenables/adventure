"""Search command for the adventure game."""

from adventure.game import Game
from .command_response import CommandResponse


def search(game: Game, *args, **kwargs) -> CommandResponse:
    """Search the room for items."""
    response = CommandResponse()
    response.add_message(
        "An exhaustive search of the room reveals the following items:", "green"
    )
    if len(game.current_loc.contents) == 0:
        response.add_message("*nothing*", "yellow")
    else:
        for item in game.current_loc.contents:
            response.add_message(f"*{item.name}*", "blue")
    return response
