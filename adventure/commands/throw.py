"""Throw an item command."""

from adventure.game import Game
from adventure.constants import self_words
from adventure.items.item import ThrowableItem
from .command_response import CommandResponse


def throw(game: Game, *args, **kwargs) -> CommandResponse:
    """Throw an item from inventory to the room."""
    thrown_thing = None
    target = None
    if len(args[0]) == 0:
        return CommandResponse("You throw your hands out into the air.", "yellow")
    else:
        thrown_thing = args[0].pop(0)
        if not game.player.inventory.holding(thrown_thing):
            return CommandResponse(f"You don't have a {thrown_thing} to throw.", "red")
        else:
            item_list = game.player.inventory.find_item(thrown_thing)

        if not isinstance(item_list[0].get("what"), ThrowableItem):
            return CommandResponse(
                f"The {thrown_thing} is not something you can throw.", "red"
            )

        if "at" in args[0]:
            target_name = args[0].pop(args[0].index("at") + 1)
            target = None
            found_target = [
                item
                for item in game.current_loc.contents
                if item.name.lower() == target_name
            ]
            if found_target:
                target = found_target[0]
            if target_name in self_words:
                return CommandResponse(
                    f"You bounce a {thrown_thing} off your own head.", "yellow"
                )
            if target_name not in [
                item.name.lower() for item in game.current_loc.contents
            ]:
                return CommandResponse(
                    f"You can't throw a {thrown_thing} at a {target_name} because it isn't here.",
                    "red",
                )

        for found in item_list:
            container_name = found.get("where")
            item = found.get("what")
            container = game.player.inventory.get(container_name)
            container.remove(item)
            game.current_loc.contents.append(item)
            if target:
                # make the effect of hitting the target with thrown item here
                return CommandResponse(
                    f"You throw a {found.get('what').name} at a {target.name}.",
                    "yellow",
                )
            else:
                return CommandResponse(
                    f"You throw a {found.get('what').name} from {container.short_desc}.",
                    "yellow",
                )
