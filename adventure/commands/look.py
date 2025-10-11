"""Player look action."""

from adventure.game import Game
from adventure.rooms.room import Room
from adventure.constants import self_words, visibility_mod_words
from adventure.exceptions import ItemNotFoundError
from .command_response import CommandResponse


def look(game: Game, *args, **kwargs) -> CommandResponse:
    """Look at things held or in the room."""
    room: Room = game.current_loc if game else None
    if not room:
        raise ItemNotFoundError("Game not initialized or current location not set.")
    response = CommandResponse()
    if not args or not args[0]:
        # look around the room
        response.add_message("You look around the room.", "yellow")
        response.add_message(room.describe(), "blue")
        if room.room_is_lit():
            response.add_message(f"Exits: {room.show_doors()}", "magenta")
        return response
    for word in args[0]:
        if word in visibility_mod_words:
            args[0].remove(word)
    if len(args[0]) > 0:
        thing_name = args[0].pop()
        if thing_name in self_words:
            response.add_message("You look at yourself.", "yellow")
            response.add_message(
                "You've certainly looked better but you're not bad.", "blue"
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
                response.add_message(f"You don't see {thing_name} here.", "red")
                return response
        if len(found) > 0:
            for item in found:
                response.add_message(
                    f"It is {item['what'].long_desc} ({item['where']}) - [{item['what'].name}]\n",
                    "green",
                )
            return response
