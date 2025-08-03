"""adventure/wall. -- And now back to the wall."""

from dataclasses import dataclass
from adventure.items.item import Item
from adventure.direction import Direction
from adventure.door import Door


@dataclass(kw_only=True)
class Wall(Item):
    """This is what a wall looks like."""

    location: Direction
    doors: list[Door]

    def add_door(self, door: Door):
        self.doors.append(door)
