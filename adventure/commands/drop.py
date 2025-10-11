"""Drop an item command."""

from adventure.game import Game
from adventure.exceptions import ItemNotFoundError, ContainerNotFoundError
from .command_response import CommandResponse


def drop(game: Game, *args, **kwargs) -> CommandResponse:
    """Drop an item from inventory to the room."""
    if not args or not args[0]:
        return CommandResponse("You drop nothing like a bad habit.", "yellow")
    if "all" in args[0]:
        # We'll interpret this as dropping what we're holding, not all bags.
        response = CommandResponse()
        try:
            hands = game.player.inventory.get("hands")
            if not hands.is_empty():
                response.add_message("You dropped:\n", "yellow")
                for item in hands.contents:
                    hands.contents.remove(item)
                    game.current_loc.contents.append(item)
                    response.add_message(f"A {item.name}\n", "yellow")
        except ContainerNotFoundError:
            # We'll assume they know they're missing a hand if they are...
            return CommandResponse("You don't have a free hand to drop that.", "red")
        return response
    else:
        response = CommandResponse()
        for item_name in args[0]:
            found = False
            for container in game.player.inventory.containers:
                try:
                    found = container.get(item_name)
                    response.add_message("You dropped:\n", "yellow")
                    container.remove(found)
                    game.current_loc.contents.append(found)
                    response.add_message(
                        f"A {found.name} from {container.short_desc}.", "yellow"
                    )
                    return response
                except ItemNotFoundError:
                    continue
            if found is False:
                return CommandResponse(f"You couldn't find {item_name} to drop.", "red")
