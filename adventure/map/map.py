"""adventure/map -- a class to handle the world in which the player roams."""

import os
from dataclasses import dataclass, field
from adventure.rooms.room import Room
from adventure.rooms.room_loader import load_room_from_yaml
from adventure.exceptions import BadYamlError
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.defaults import DEFAULT_DATA_DIR


@dataclass(kw_only=True)
class Map:
    """The map of the adventure world."""

    file_name: str = field(default="")
    base_data_dir: str = field(default=DEFAULT_DATA_DIR)
    name: str = "Adventure Map"
    description: str = "A map of the adventure world."
    start_room: int = 1  # index of the starting room
    rooms: dict[str, Room] = field(default_factory=dict)

    def __init__(self, base_data_dir: str, file_name: str):
        if not os.path.isdir(base_data_dir):
            raise NotADirectoryError(f"Base data directory not found: {base_data_dir}")
        self.base_data_dir = base_data_dir
        if not file_name:
            raise ValueError("A map file name must be provided.")
        map_path = f"{base_data_dir}/{file_name}"
        if not os.path.isfile(map_path):
            raise FileNotFoundError(f"Map file not found: {map_path}")
        self.file_name = map_path
        self.rooms = {}  # Initialize rooms as an empty dictionary
        self.load_yaml()

    def __str__(self):
        return f"{self.name} - {self.description}"

    def get_room(self, room_index: int) -> Room:
        """Get a room by its index in the map.

        Args:
         - room_index (int): The index of the room to retrieve.

        Returns:
         - Room: The room at the specified index.

        Raises:
         - IndexError: If the index is out of bounds.

        """
        if room_index in self.rooms:
            return self.rooms[room_index]
        raise IndexError("Room index out of bounds.")

    def load_yaml(self):
        """Load rooms from a YAML document.

        Args:
         - yaml_doc (str): The path to the YAML document containing room definitions.

        """
        try:
            map_data = get_yaml_doc(self.file_name)
        except BadYamlError as bye:
            raise bye from bye

        self.name = map_data.get("name", "Adventure Map")
        self.description = map_data.get("description", "A map of the adventure world.")
        self.start_room = map_data.get("start_room", 1)

        # Load room files listed in the map document
        for room_data in map_data.get("rooms", []):
            room = load_room_from_yaml(
                f"{self.base_data_dir}/rooms/{room_data['file']}.yml"
            )
            if not room_data.get("id"):
                raise ValueError(
                    "Room ID Unset: Each room in map YAML must have a unique 'id' field."
                )
            if room_data["id"] in self.rooms:
                raise ValueError(
                    f"Duplicate room id {room_data['id']} found in map YAML."
                )
            self.rooms[room_data["id"]] = room
            room_exits = room_data.get("exits", {})
            room.connect_exits(exit_map=room_exits)
