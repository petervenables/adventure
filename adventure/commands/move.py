"""Player movement action."""

from adventure.game import Game
from adventure.rooms.room import Room
from adventure.map.direction import Direction
from adventure.constants import mobility_mod_words
from .command_response import CommandResponse


def move(game: Game, *args, **kwargs) -> CommandResponse:
    """Move the player around the map."""
    action = kwargs.get("action")
    if len(args[0]) == 0:
        return CommandResponse(f"You {action} about the room.", "blue")
    for word in args[0]:
        if word in mobility_mod_words:
            args[0].remove(word)
    if len(args[0]) == 0:
        return CommandResponse(f"You {action} about the room.", "blue")
    try:
        direction = Direction.from_string(args[0].pop())
    except KeyError:
        return CommandResponse(f"You can't {action} that way.")
    room: Room = game.current_loc if game else None
    if not room:
        return CommandResponse(
            "You can't move because the current location is not set.", "red"
        )
    # Find the exit matching the direction
    exit_match = next(
        (
            exit
            for exit in room.get_exits()
            if direction.name.lower() == exit.location.name.lower()
        ),
        None,
    )
    if not exit_match:
        return CommandResponse(f"You don't see how you can {action} that way.", "red")

    # Check for an open door leading somewhere
    for door in exit_match.doors:
        if door.is_open:
            if door.leads_to is not None:
                response = CommandResponse()
                game.current_loc = game.map.get_room(door.leads_to)
                response.add_message(
                    f"You {action} {direction.name.lower()} through the {door.name}.\n",
                    "yellow",
                )
                response.add_message(game.current_loc.describe(), "blue")
                game.current_loc.visit()
                if game.current_loc.room_is_lit():
                    response.add_message(
                        f"Exits: {game.current_loc.show_doors()}", "magenta"
                    )
                return response
            return CommandResponse(f"You can't {action} that way.", "red")
        else:
            return CommandResponse(
                f"The {door.name} is closed. You can't {action} that way until you open it.",
                "red",
            )

    return CommandResponse(
        f"You attempt to {action} in that direction but are stopped by an invisible force.",
        "red",
    )
