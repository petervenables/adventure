"""Throw an item command."""

from adventure.game import Game
from adventure.constants import SELF_WORDS
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
            thrown_item = game.player.inventory.pull_item(thrown_thing)
            game.current_loc.contents.append(thrown_item)

        if not isinstance(thrown_item, ThrowableItem):
            return CommandResponse(
                f"The {thrown_thing} is not something you can throw. (but can be dropped)",
                "red",
            )

        if len(args[0]) > 0:
            target_name = args[0].pop(0)
            # if "at" in args[0]:
            #    target_name = args[0].pop(args[0].index("at") + 1)
            if target_name in SELF_WORDS:
                return CommandResponse(
                    f"You bounce a {thrown_thing} off your own head.", "yellow"
                )
            target = None
            found_target = [
                item
                for item in game.current_loc.contents
                if item.name.lower() == target_name
            ]
            if found_target:
                target = found_target[0]
            if target_name and not target:
                return CommandResponse(
                    f"You can't throw a {thrown_thing} at a {target_name} because it isn't here.",
                    "red",
                )
            if target_name and target:
                # make the effect of hitting the target with thrown item here
                return CommandResponse(
                    f"You throw a {thrown_thing} at a {target.name}.",
                    "yellow",
                )
            else:
                return CommandResponse(
                    f"You throw a {thrown_thing}.",
                    "yellow",
                )
