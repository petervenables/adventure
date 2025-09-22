"""adventure/wall. -- And now back to the wall."""

from dataclasses import dataclass
from adventure.items.item import Item
from adventure.map.direction import Direction
from adventure.rooms.door import Door


@dataclass(kw_only=True)
class Wall(Item):
    """This is what a wall looks like."""

    location: Direction
    doors: list[Door]

    def add_door(self, door: Door):
        """Add a door to this wall."""
        self.doors.append(door)

    def has_door(self) -> bool:
        """Checks if this wall has a door."""
        return len(self.doors) > 0

    def get_door(self) -> Door | None:
        """Get the first door on this wall, if any."""
        if self.has_door():
            return self.doors[0]
        return None
