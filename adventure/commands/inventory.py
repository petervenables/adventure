"""Inventory Command."""

from adventure.game import Game
from .command_response import CommandResponse


def inv(game: Game, *args, **kwargs) -> CommandResponse:
    """Display the things you have on hand."""
    contents = game.player.inventory.list_all_contents()
    if not contents:
        return CommandResponse("Your inventory is empty.", "yellow")
    response = CommandResponse()
    response.add_message(f"You are carrying:{contents}", "blue")
    return response
