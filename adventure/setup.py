"""adventure/setup. -- possibly temporary methods to define static rooms and things."""
from adventure.room import Room
from adventure.wall import Wall
from adventure.direction import Direction
from adventure.door import Door
from adventure.item import RoomItem, SizeCategory
from adventure.dao.doc_yaml import get_yaml_doc

def start_room() -> Room:
    """Create a starting room."""
    room_dict = get_yaml_doc("adventure/data/rooms/start_room.yml")
    room = Room(
        name=room_dict.get("name"),
        short=room_dict.get("short_desc"),
        long=room_dict.get("long_desc"),
    )
    for direction in room_dict.get("walls"):
        location = Direction(str.capitalize(direction['name']), [])
        wall_dict = get_yaml_doc(f"adventure/data/walls/{direction['type']}.yml")
        wall = Wall(
            location=location,
            name=f"{location.name} wall",
            short_desc=wall_dict['short_desc'],
            long_desc=wall_dict['long_desc'],
            doors=[]
        )
        if direction.get("door", None) is not None:
            door_dict = get_yaml_doc(f"adventure/data/doors/{direction['door']}.yml")
            door = Door(
                name=door_dict['name'],
                short_desc=door_dict['short_desc'],
                long_desc=door_dict['long_desc']
            )
            wall.add_door(door)
        room.walls.append(wall)
    return room

def start_rock() -> RoomItem:
    """This is our test rock. We like it."""
    rock = RoomItem(
        name="rock",
        short_desc="a fist-sized rock.",
        long_desc="This is an unremarkable fist-sized rock although it has a very satisfying heft to it.",
        weight=1,
        size=SizeCategory(
            name="small",
            bulk=1,
            is_handheld=True,
            is_moveable=True,
            is_liftable=True
            )
        )
    return rock
