"""adventure/room -- a class to handle rooms the player will traverse."""

from dataclasses import dataclass, field
from typing import Dict, List
from adventure.rooms.wall import Wall
from adventure.rooms.door import Door
from adventure.map.direction import Direction
from adventure.items.item import Item
from adventure.exceptions import ItemNotFoundError
from adventure.items.item import LightSourceItem
from adventure.rooms.events import RoomEvent


@dataclass(kw_only=True)
class Room:
    """Define what it is that the player traverses."""

    name: str
    short_desc: str
    long_desc: str
    walls: List[Wall] = field(default_factory=list)
    contents: List[Item] = field(default_factory=list)
    inhabitants: List = field(default_factory=list)
    switches: List[Item] = field(default_factory=list)
    visited: bool = False
    events: List[RoomEvent] = field(default_factory=list)
    is_lit: bool = False  # If True, the room is always lit

    def describe(self, thorough: bool = False) -> str:
        """Return a description of the room depending on if it has been visited."""
        if not self.room_is_lit():
            return "The room is shrouded in darkness. You can't see anything."
        if not self.visited or thorough:
            return self.long_desc
        return self.short_desc

    def visit(self):
        """Mark the room as visited."""
        self.visited = True

    def add_wall(self, wall: Wall, location: Direction):
        """Add a wall to the room."""
        if len(self.walls) <= 0:
            # indexed at 1 to match Direction enum (walls[0] is always None)
            self.walls = [None for _ in range(len(Direction))]
        self.walls[int(location)] = wall

    def get_walls(self) -> List[Wall]:
        """Get the list of walls in this room."""
        return [wall for wall in self.walls if wall is not None]

    def add_door(self, door: Door, location: Direction):
        """Add a door to a wall in the room."""
        for wall in self.get_walls():
            if wall.location.name == location.name:
                wall.add_door(door)

    def show_doors(self) -> str:
        """Get the list of doors in this room."""
        out_str: str = ""
        for wall in self.get_walls():
            if wall.has_door():
                out_str += f"[ {wall.location.name} ]"
        return out_str

    def get_doors(self) -> list[Door]:
        """Get a list of doors in this room."""
        doors = []
        for wall in self.get_walls():
            if wall.has_door():
                doors.append(wall.doors[0])
        return doors

    def get_exits(self) -> list[Wall]:
        """Get a list of walls with doors."""
        exits = []
        for wall in self.get_walls():
            if wall.has_door():
                exits.append(wall)
        return exits

    def get_direction_of_door(self, door_name: str) -> Direction | None:
        """Get the direction of a door by its name."""
        for wall in self.get_walls():
            door = wall.get_named_door(door_name)
            if door:
                return wall.location
        return None

    def get_everything(self) -> List[str]:
        """Get a list of all items and doors in the room."""
        everything = [item.name.lower() for item in self.contents]
        everything.extend([wall.name.lower() for wall in self.get_exits()])
        everything.extend([door.name.lower() for door in self.get_doors()])
        return everything

    def connect_exits(self, exit_map: Dict[str, int]):
        """Connect the doors in this room to other rooms based on the exit map.

        Arguments:
         - exit_map (Dict[Direction, int]): A mapping of directions to room IDs.

        """
        for link in exit_map:
            loc = Direction.from_string(link)
            if self.walls[int(loc)].has_door():
                # Still considering that a wall should only have one door.
                self.walls[int(loc)].doors[0].connect(exit_map[link])

    def in_room(self, item_name: str) -> List[Dict[str, Item]]:
        """Checks the Items in the room and returns a list of those that match the named thing.

        Arguments:
         - item_name(str):          The name of the item to be found.

        Returns:
         - List[Dict[str, Item]]:   The location and the found item if it is there.

        Raises:
         - (ItemNotFoundError):     If the Item is not in the room.

        """
        found = []
        item_lower = item_name.lower()
        for item in self.contents:
            if item_lower == item.name.lower():
                found.append({"where": "room", "what": item})
        for wall in self.get_walls():
            if item_lower == wall.location.name.lower():
                if wall.has_door():
                    found.append({"where": wall.location.name, "what": wall.get_door()})
                else:
                    found.append({"where": wall.location.name, "what": wall})
            elif item_lower in [door.name.lower() for door in wall.doors]:
                for door in wall.doors:
                    if item_lower == door.name.lower():
                        found.append({"where": wall.location.name, "what": door})
        if len(found) > 0:
            return found
        raise ItemNotFoundError(f"Item {item_name} not in room.")

    def activate(self):
        """Activate any events associated with this room."""
        for event in self.events:
            if event.is_triggered(self):
                event.fire(self)

    def room_is_lit(self) -> bool:
        """Return True if the room is lit, False if it is dark."""
        # Some rooms are always lit
        if self.is_lit:
            return True
        # A room is lit if it has at least one light source that is on
        for item in self.contents:
            if isinstance(item, LightSourceItem) and item.is_lit():
                return True
        return False
