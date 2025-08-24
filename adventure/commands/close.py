"""Close command for the adventure game."""

from adventure.rooms.room import Room


def close(game, *args, **kwargs):
    """Close a door in the current room."""
    if not args or not args[0]:
        return "You only know how to close things that can be closed. Indicate something to close."

    for close_tgt in args[0]:
        found = False
        room: Room = game.current_loc
        directions = [wall.location.name.lower() for wall in room.walls]
        if close_tgt.lower() in directions:
            for wall in room.walls:
                if close_tgt.lower() == wall.location.name.lower():
                    if len(wall.doors) == 0:
                        return f"There are no doors on the {wall.location.name} wall to close."
                    found = True
                    for door in wall.doors:
                        if door.is_open:
                            door.close()
                            return f"You closed the {door.name}."
                        else:
                            return f"The {door.name} is already closed."
        for door in room.get_doors():
            if door.name == close_tgt:
                found = True
                if door.is_open:
                    door.close()
                    return f"You closed the {door.name}."
                else:
                    return f"The {door.name} is already closed."
        if not found:
            return f"You couldn't find a door named {close_tgt} to close."
    return "You didn't specify any doors to close."
