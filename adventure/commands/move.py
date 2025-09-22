"""Player movement action."""

from adventure.rooms.room import Room
from adventure.map.direction import Direction
from adventure.constants import mobility_mod_words


def move(game, *args, **kwargs) -> str:
    """Move the player around the map."""
    action = kwargs.get("action")
    if len(args[0]) == 0:
        return f"You {action} about the room."
    for word in args[0]:
        if word in mobility_mod_words:
            args[0].remove(word)
    if len(args[0]) == 0:
        return f"You {action} about the room."
    try:
        direction = Direction.from_string(args[0].pop())
    except KeyError as e:
        raise KeyError(f"You can't {action} that way.") from e
    room: Room = game.current_loc if game else None
    if not room:
        return "You can't move because the current location is not set."
    for wall in room.get_exits():
        if direction.name.lower() == wall.location.name.lower():
            for door in wall.doors:
                if door.is_open:
                    if door.leads_to is not None:
                        game.current_loc = game.map.get_room(door.leads_to)
                        return f"You {action} through the {door.name} to {game.current_loc.name}."
                    return f"You can't {action} that way."
                return f"The {door.name} is closed. You can't {action} that way until you open it."
            return f"You attempt to {action} in that direction but are stopped by an invisible force."
    return f"You don't see how you can {action} that way."
