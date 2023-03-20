"""adventure/wall. -- And now back to the wall."""
from typing import List
from dataclasses import dataclass
from adventure.item import Item
from adventure.direction import Direction
from adventure.door import Door

@dataclass
class Wall(Item):
    """This is what a wall looks like."""
    location: Direction
    doors: List[Door]

    def add_door(self, door: Door):
        self.doors.append(door)
