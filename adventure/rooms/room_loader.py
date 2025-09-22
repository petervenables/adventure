"""Module to load Room objects from YAML files."""

from adventure.rooms.room import Room
from adventure.rooms.wall import Wall
from adventure.map.direction import Direction
from adventure.rooms.door import Door
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.items.item_loader import load_item_from_yaml
from adventure.defaults import DEFAULT_DATA_DIR
from adventure.exceptions import BadYamlError

CLASS_MAP = {}


def load_room_from_yaml(file_path: str) -> Room:
    """Load a room from a YAML file."""
    data = get_yaml_doc(file_path)
    if not data:
        raise BadYamlError(f"Failed to load or parse YAML file: {file_path}")

    base_classes = [Room]
    for cls_name in data.get("classes", []):
        if cls_name not in CLASS_MAP:
            raise ValueError(f"Unknown room class: {cls_name}")
        cls = CLASS_MAP[cls_name]
        if cls:
            for i, base in enumerate(base_classes):
                if issubclass(cls, base):
                    base_classes[i] = cls
                    break
            else:
                base_classes.append(cls)
    composite_item = type(
        data["name"].capitalize().replace(" ", "_") + "Room", tuple(base_classes), {}
    )
    args = {
        key: value
        for key, value in data.items()
        if key not in ["walls", "contains", "inhabitants"]
    }
    room = composite_item(**args)
    for direction in data.get("walls"):
        location = Direction.from_string(direction["name"])
        wall_dict = get_yaml_doc(f"{DEFAULT_DATA_DIR}/walls/{direction['type']}.yml")
        wall = Wall(
            location=location,
            name=f"{location.name} wall",
            short_desc=wall_dict["short_desc"],
            long_desc=wall_dict["long_desc"],
            doors=[],
        )
        if direction.get("door") is not None:
            door_dict = get_yaml_doc(
                f"{DEFAULT_DATA_DIR}/doors/{direction['door']}.yml"
            )
            door = Door(
                name=door_dict.get("name"),
                short_desc=door_dict.get("short_desc"),
                long_desc=door_dict.get("long_desc"),
            )
            wall.add_door(door)
        room.add_wall(wall=wall, location=location)
    if data.get("contains") is not None:
        for item_data in data.get("contains", []):
            item = load_item_from_yaml(f"{DEFAULT_DATA_DIR}/things/{item_data}.yml")
            room.contents.append(item)
    return room
