"""adventure/room -- a class to handle rooms the player will traverse."""
from typing import Dict, List
from adventure.wall import Wall
from adventure.door import Door
from adventure.direction import Direction
from adventure.item import Item
from adventure.exceptions import ItemNotFoundError

class Room:
    """Define what it is that the player traverses."""
    name: str
    short_desc: str
    long_desc: str
    walls: List[Wall] = []
    contents: List[Item] = []
    inhabitants: List = []

    def __init__(self, name: str, short: str, long: str):
        self.name = name
        self.short_desc = short
        self.long_desc = long

    def add_door(self, door: Door, location: Direction):
        """Add a door to a wall in the room."""
        for wall in self.walls:
            if wall.location == location.name or wall.location in location.aliases:
                wall.doors.append(door)

    def show_doors(self) -> str:
        """Get the list of doors in this room."""
        out_str: str = ""
        for wall in self.walls:
            for door in wall.doors:
                out_str += f"[ {door.name}, {wall.location.name} ]"
        return out_str

    def get_doors(self) -> List[Wall]:
        """Get a list of walls with doors."""
        doors = []
        for wall in self.walls:
            if len(wall.doors) > 0:
                doors.append(wall)
        return doors

    def in_room(self, item_name: str) -> List[Dict[str, Item]]:
        """Checks the Items in the room and returns a list of those that match the named thing.
        
        Arguments:
         - item_name(str):          The name of the item to be found.

        Returns:
         - List[Dict[str, Item]]:   The location and the found item if it is there.

        Raises:
         - (ItemNotFoundError):     If the Item is not in the room.
        
        """
        items = []
        for item in self.contents:
            if item_name.lower() == item.name.lower():
                items.append({"where": "room", "what": item})
        for wall in self.walls:
            if item_name.lower() == wall.location.name.lower():
                if len(wall.doors) > 0:
                    for door in wall.doors:
                        items.append({"where": wall.location.name.lower(), "what": door})
                else:
                    items.append({"where": wall.location.name.lower(), "what": wall})
        if len(items) > 0:
            return items
        raise ItemNotFoundError(f"Item {item_name} not in room.")
