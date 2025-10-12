"""Player look action."""

from adventure.game import Game
from adventure.rooms.room import Room
from adventure.constants import SELF_WORDS, VISIBILITY_MOD_WORDS
from adventure.exceptions import ItemNotFoundError
from .command_response import CommandResponse


def examine(game: Game, *args, **kwargs) -> CommandResponse:
    """Carefully scrutinze things held or in the room."""
    room: Room = game.current_loc if game else None
    if not room:
        raise ItemNotFoundError("Game not initialized or current location not set.")
    response = CommandResponse()
    if not args or not args[0] or "room" in args[0]:
        # look around the room
        response.add_message("You carefully examine the room.", "yellow")
        response.add_message(room.describe(thorough=True), "blue")
        if room.room_is_lit():
            response.add_message("Exits: " + room.show_doors(), "magenta")
        return response
    for word in args[0]:
        if word in VISIBILITY_MOD_WORDS:
            args[0].remove(word)
    if len(args[0]) > 0:
        thing_name = args[0].pop()
        if thing_name in SELF_WORDS:
            response.add_message("You examine yourself...", "yellow")
            response.add_message(
                "You've certainly looked better but you're not bad.", "blue"
            )
            # when examining self, show conditions
            # BUT we can't do that yet.
            # when examining self, show inventory
            response.add_message(
                "You are carrying: " + game.player.inventory.list_all_contents(), "blue"
            )
            return response
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
