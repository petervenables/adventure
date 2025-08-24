"""adventure/setup. -- possibly temporary methods to define static rooms and things."""

from adventure.rooms.room import Room
from adventure.rooms.wall import Wall
from adventure.direction import Direction
from adventure.rooms.door import Door
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.items.item_loader import load_item_from_yaml


def start_room() -> Room:
    """Create a starting room."""
    room_dict = get_yaml_doc("adventure/data/rooms/start_room.yml")
    room = Room(
        name=room_dict.get("name"),
        short_desc=room_dict.get("short_desc"),
        long_desc=room_dict.get("long_desc"),
    )
    for direction in room_dict.get("walls"):
        location = Direction(str.capitalize(direction["name"]), [])
        wall_dict = get_yaml_doc(f"adventure/data/walls/{direction['type']}.yml")
        wall = Wall(
            location=location,
            name=f"{location.name} wall",
            short_desc=wall_dict["short_desc"],
            long_desc=wall_dict["long_desc"],
            doors=[],
        )
        if direction.get("door", None) is not None:
            door_dict = get_yaml_doc(f"adventure/data/doors/{direction['door']}.yml")
            door = Door(
                name=door_dict["name"],
                short_desc=door_dict["short_desc"],
                long_desc=door_dict["long_desc"],
            )
            wall.add_door(door)
        room.walls.append(wall)
    for contained_item in room_dict.get("contains", []):
        item = load_item_from_yaml(f"adventure/data/things/{contained_item}.yml")
        room.contents.append(item)
    return room
