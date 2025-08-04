"""Throw an item command."""

from typing import Union
from adventure.constants import self_words


def throw(game, *args, **kwargs) -> Union[str | None]:
    """Throw an item from inventory to the room."""
    thrown_thing = None
    target = None
    if len(args[0]) == 0:
        return "You throw your hands out into the air."
    else:
        thrown_thing = args[0].pop(0)
        if not game.player.inventory.holding(thrown_thing):
            return f"You don't have {thrown_thing} to throw."
        else:
            item_list = game.player.inventory.find_item(thrown_thing)
        if "at" in args[0]:
            target_name = args[0].pop(args[0].index("at") + 1)
            if target_name in self_words:
                return f"You bounce {thrown_thing} off your own head."
            if target_name not in game.current_loc.contents:
                return f"You can't throw {thrown_thing} at {target_name} because it isn't here."

        for found in item_list:
            container_name = found.get("where")
            item = found.get("what")
            container = game.player.inventory.get(container_name)
            container.remove(item)
            game.current_loc.contents.append(item)
            if target:
                return f"You throw {found.get('what').name} from {container.short_desc} at {target_name}."
            else:
                return f"You throw {found.get('what')} from {container.short_desc}."
