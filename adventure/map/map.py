"""adventure/map -- a class to handle the world in which the player roams."""

from dataclasses import dataclass, field
import yaml
from adventure.rooms.room import Room


@dataclass(kw_only=True)
class Map:
    """The map of the adventure world."""

    name: str = "Adventure Map"
    description: str = "A map of the adventure world."
    start_room: Room = None
    rooms: list[Room] = field(default_factory=list)

    def __str__(self):
        return f"{self.name} - {self.description}"

    def insert_room(self, room: Room) -> int:
        """Insert a room into the map.

        Args:
         - room (Room): The room to be added to the map.

        Returns:
         - int: The index of the newly added room.

        """
        self.rooms.append(room)
        if len(self.rooms) == 1:
            self.start_room = room
        return len(self.rooms)

    def get_room(self, room_index: int) -> Room:
        """Get a room by its index in the map.

        Args:
         - room_index (int): The index of the room to retrieve.

        Returns:
         - Room: The room at the specified index.

        Raises:
         - IndexError: If the index is out of bounds.

        """
        if 0 <= room_index < len(self.rooms):
            return self.rooms[room_index]
        raise IndexError("Room index out of bounds.")

    def load_yaml(self, yaml_doc: str):
        """Load rooms from a YAML document.

        Args:
         - yaml_doc (str): The path to the YAML document containing room definitions.

        """
        from adventure.rooms.room_loader import load_room_from_yaml

        with open(yaml_doc, "r", encoding="utf8") as file:
            # read the YAML into a dictionary
            data = yaml.safe_load(file)
            for room_data in data.get("rooms", []):
                room = load_room_from_yaml(f"adventure/data/rooms/{room_data}.yml")
                self.insert_room(room)
