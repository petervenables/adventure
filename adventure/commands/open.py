"""Open command for the adventure game."""

from adventure.rooms.room import Room


def open_cmd(game, *args, **kwargs):
    """Open a door in the current room."""
    if not args or not args[0]:
        return "You only know how to open things that can be opened. Indicate something to open."

    for open_tgt in args[0]:
        found = False
        room: Room = game.current_loc
        directions = [wall.location.name.lower() for wall in room.walls]
        if open_tgt.lower() in directions:
            for wall in room.walls:
                if open_tgt.lower() == wall.location.name.lower():
                    if len(wall.doors) == 0:
                        return f"There are no doors on the {wall.location.name} wall to open."
                    found = True
                    for door in wall.doors:
                        if not door.is_open:
                            door.open()
                            return f"You opened the {door.name}."
                        else:
                            return f"The {door.name} is already opened."
        for door in room.get_doors():
            if door.name == open_tgt:
                found = True
                if not door.is_open:
                    door.open()
                    return f"You opened the {door.name}."
                else:
                    return f"The {door.name} is already opened."
        if not found:
            return f"You couldn't find a door named {open_tgt} to open."
    return "You didn't specify any doors to open."
