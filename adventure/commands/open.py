"""Open command for the adventure game."""

from adventure.game import Game
from adventure.rooms.room import Room
from .command_response import CommandResponse


def open_cmd(game: Game, *args, **kwargs) -> CommandResponse:
    """Open a door in the current room."""
    if not args or not args[0]:
        return CommandResponse(
            "You only know how to open things that can be opened. Indicate something to open.",
            "red",
        )

    for open_tgt in args[0]:
        found = False
        room: Room = game.current_loc
        directions = [
            wall.location.name.lower() for wall in room.get_walls() if wall.has_door()
        ]
        if open_tgt.lower() in directions:
            for wall in room.get_walls():
                if open_tgt.lower() == wall.location.name.lower():
                    found = True
                    for door in wall.doors:
                        if not door.is_open:
                            door.open()
                            return CommandResponse(
                                f"You opened the {door.name}.", "blue"
                            )
                        else:
                            return CommandResponse(
                                f"The {door.name} is already opened.", "yellow"
                            )
        for door in room.get_doors():
            if open_tgt in door.aka():
                found = True
                if not door.is_open:
                    door.open()
                    return CommandResponse(f"You opened the {door.name}.", "blue")
                else:
                    return CommandResponse(
                        f"The {door.name} is already opened.", "yellow"
                    )
        if not found:
            return CommandResponse(
                f"You couldn't find a door named {open_tgt} to open.", "red"
            )
    return CommandResponse("You didn't specify any doors to open.", "red")
