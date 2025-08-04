"""Search command for the adventure game."""


def search(game, *args, **kwargs):
    """Search the room for items."""
    output = "An exhaustive search of the room reveals the following items:\n"
    if len(game.current_loc.contents) == 0:
        output += "*nothing*"
    else:
        for item in game.current_loc.contents:
            output += f"*{item.name}*"
    return output
