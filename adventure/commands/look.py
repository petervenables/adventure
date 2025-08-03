"""Player look action."""

from .command import Command


class LookCmd(Command):
    """Class to handle the 'look' action in the game."""


def look(game, args):
    """Simulate the 'look' command in the game."""
    if not args:
        return "You look around and see nothing of interest."
    else:
        thing = args[0]
        # should probably generalize this to taking an item as an argument and let the game search for it first
        if thing in game.items:
            return f"You look at the {thing} and see: {game.items[thing].description}"
        else:
            return f"{thing} does not seem to be here."
