"""Pick command for the adventure game."""

from adventure.game import Game
from adventure.items.item import HandheldItem
from .command_response import CommandResponse


def pick(game: Game, *args, **kwargs) -> CommandResponse:
    """Obtain an item from the room."""
    action = kwargs.get("action")
    if not args or not args[0]:
        return CommandResponse("You pick your nose, briefly.", "yellow")
    if "up" in args[0]:
        args[0].remove("up")
    for item in game.current_loc.contents:
        if item.name.lower() in args[0]:
            if not isinstance(item, HandheldItem):
                return CommandResponse(
                    f"The {item.name} is not something you can {action}.", "red"
                )
            if item.weight <= 100:
                if game.player.inventory.can_hold("hands", item):
                    game.player.inventory.insert_into("hands", item)
                    game.current_loc.contents.remove(item)
                    return CommandResponse(f"You pick up a {item.name}.", "yellow")
                else:
                    return CommandResponse(
                        "You don't have a free hand to pick that up.", "red"
                    )
            else:  # If the item is too heavy
                return CommandResponse(
                    f"The {item.name} is too heavy for you to pick up.", "red"
                )
    return CommandResponse("You don't see that here.", "yellow")
