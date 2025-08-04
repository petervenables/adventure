"""Pick command for the adventure game."""


def pick(game, *args, **kwargs) -> str:
    """Obtain an item from the room."""
    if not args or not args[0]:
        return "You pick your nose, briefly."
    if "up" in args[0]:
        args[0].remove("up")
    for item in game.current_loc.contents:
        if item.name.lower() in args[0]:
            if item.weight <= 100:
                if game.player.inventory.can_hold("hands", item):
                    game.player.inventory.insert_into("hands", item)
                    game.current_loc.contents.remove(item)
                    return f"You pick up {item.name}."
                else:
                    return "You don't have a free hand to pick that up."
            else:  # If the item is too heavy
                return f"The {item.name} is too heavy for you to pick up."
    return "You don't see that here."
