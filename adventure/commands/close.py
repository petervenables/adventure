"""Close command for the adventure game."""

from adventure.game import Game
from adventure.rooms.room import Room
from .command_response import CommandResponse


def close(game: Game, *args, **kwargs) -> CommandResponse:
    """Close a door in the current room."""
    if not args or not args[0]:
        return CommandResponse(
            "You only know how to close things that can be closed. Indicate something to close.",
            "red",
        )

    for close_tgt in args[0]:
        found = False
        room: Room = game.current_loc
        directions = [
            wall.location.name.lower() for wall in room.get_walls() if wall.has_door()
        ]
        if close_tgt.lower() in directions:
            for wall in room.get_walls():
                if close_tgt.lower() == wall.location.name.lower():
                    found = True
                    for door in wall.doors:
                        if door.is_open:
                            door.close()
                            return CommandResponse(
                                f"You closed the {door.name}.", "blue"
                            )
                        else:
                            return CommandResponse(
                                f"The {door.name} is already closed.", "yellow"
                            )
        for door in room.get_doors():
            if door.name == close_tgt:
                found = True
                if door.is_open:
                    door.close()
                    return CommandResponse(f"You closed the {door.name}.", "blue")
                else:
                    return CommandResponse(
                        f"The {door.name} is already closed.", "yellow"
                    )
        if not found:
            return CommandResponse(
                f"You couldn't find a door named {close_tgt} to close.", "red"
            )
    return CommandResponse("You didn't specify any doors to close.", "red")
