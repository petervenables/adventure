"""adventure/door. -- Doors are the pathway to other rooms. So, kinda important."""

from dataclasses import dataclass
from adventure.items.item import Item


@dataclass
class Door(Item):
    """Doors are marvelous things."""

    is_open: bool = True
    is_locked: bool = False
    is_blocked: bool = False

    def lock(self):
        """Lock the door."""
        self.is_locked = True

    def unlock(self):
        """Unlock the door."""
        self.is_locked = False

    def open(self):
        """Open the door."""
        self.is_open = True

    def close(self):
        """Close the door."""
        self.is_open = False

    def block(self):
        """Make the door impassible."""
        self.is_blocked = True

    def unblock(self):
        """Unblock the door."""
        self.is_blocked = False
