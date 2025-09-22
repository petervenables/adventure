"""Player look action."""

from adventure.rooms.room import Room
from adventure.constants import self_words, visibility_mod_words
from adventure.exceptions import ItemNotFoundError


def examine(game, *args, **kwargs):
    """Carefully scrutinze things held or in the room."""
    room: Room = game.current_loc if game else None
    if not room:
        raise ItemNotFoundError("Game not initialized or current location not set.")
    if not args or not args[0]:
        # look around the room
        output = ""
        for line in room.long_desc.splitlines():
            output += line + "\n"
        output += "\nDoors: " + room.show_doors()
        return output
    for word in args[0]:
        if word in visibility_mod_words:
            args[0].remove(word)
    if len(args[0]) > 0:
        thing_name = args[0].pop()
        if thing_name in self_words:
            return "You've certainly looked better but you're not bad."
        found = []
        try:
            # Look for a describable item in the room
            for each in room.in_room(thing_name):
                found.append(each)
        except ItemNotFoundError:
            # if not in the room, perhaps we have it on hand?
            try:
                for each in game.player.inventory.find_item(thing_name):
                    found.append(each)
            except ItemNotFoundError:
                return f"You don't see {thing_name} here."
        if len(found) > 0:
            for item in found:
                return f"{item['what'].long_desc} ({item['where']}) - [{item['what'].name}]\n"
