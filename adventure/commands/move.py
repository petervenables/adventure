"""Player movement action."""

from adventure.rooms.room import Room
from adventure.constants import mobility_mod_words


def move(game, *args, **kwargs) -> str:
    """Move the player around the map."""
    if len(args[0]) == 0:
        return "You wander about the room."
    for word in args[0]:
        if word in mobility_mod_words:
            args[0].remove(word)
    if len(args[0]) == 0:
        return "You wander about the room."
    direction = args[0].pop()
    room: Room = game.current_loc if game else None
    if not room:
        return "You can't move because the current location is not set."
    for wall in room.get_doors():
        if direction.lower() == wall.location.name.lower():
            for door in wall.doors:
                if door.is_open:
                    if door.leads_to is not None:
                        game.current_loc = game.map.get_room(door.leads_to)
                        return f"You walk through the {door.name} to {game.current_loc.name}."
                    return "You can't go that way."
                return f"The {door.name} is closed. You can't go that way until you open it."
            return "You attempt to walk in that direction but are stopped by an invisible force."
    return "You don't see how you can go that way."
