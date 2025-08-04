"""Drop an item command."""

from adventure.exceptions import ItemNotFoundError, ContainerNotFoundError


def drop(game, *args, **kwargs):
    """Drop an item from inventory to the room."""
    if not args or not args[0]:
        return "You drop nothing like a bad habit."
    if "all" in args[0]:
        # We'll interpret this as dropping what we're holding, not all bags.
        output = ""
        try:
            hands = game.player.inventory.get("hands")
            if not hands.is_empty():
                output += "You dropped:\n"
                for item in hands.contents:
                    hands.contents.remove(item)
                    game.current_loc.contents.append(item)
                    output += f"*{item.name}*\n"
        except ContainerNotFoundError:
            # We'll assume they know they're missing a hand if they are...
            return
        return output
    else:
        for item_name in args[0]:
            found = False
            for container in game.player.inventory.containers:
                try:
                    found = container.get(item_name)
                    container.remove(found)
                    game.current_loc.contents.append(found)
                    output = "You dropped:\n"
                    output += f"*{found.name}* from {container.short_desc}."
                    return output
                except ItemNotFoundError:
                    continue
            if found is False:
                return f"You couldn't find {item_name} to drop."
