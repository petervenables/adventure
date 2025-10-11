"""Pick command for the adventure game."""

from adventure.game import Game
from adventure.items.item import PullableItem
from .command_response import CommandResponse


def pull(game: Game, *args, **kwargs) -> CommandResponse:
    """Obtain an item from the room."""
    action = kwargs.get("action")
    if not args or not args[0]:
        return CommandResponse(f"You need to {action} something specific.", "red")
    if "up" in args[0]:
        args[0].remove("up")
    response = CommandResponse()
    for item in game.current_loc.contents:
        # check any of the items aliases are in the args list
        if any(alias in args[0] for alias in item.aka()):
            if not isinstance(item, PullableItem):
                return CommandResponse(
                    f"The {item.name} is not something you can {action}.", "red"
                )
            response.add_message(item.toggle(), "yellow")
            response.add_message(f"You {action} the {item.name}.", "yellow")
            return response
    return CommandResponse("You don't see that here.", "yellow")
