"""adventure/item -- a class to handle things the player can pick up, move, or otherwise interact with."""
from dataclasses import dataclass

@dataclass
class SizeCategory:
    """Helps us know what we can do with this item."""
    name: str
    # Bulk is a comparable size factor where bigger items have a higher bulk
    bulk: int
    is_handheld: bool
    is_moveable: bool
    is_liftable: bool

@dataclass
class Item:
    """Items are the nonliving things we encounter in the adventure."""
    name: str
    short_desc: str
    long_desc: str

    def __str__(self):
        return f"{self.name} - {self.short_desc}"

    def __eq__(self, name: str) -> bool:
        if name == self.name:
            return True
        return False

@dataclass
class RoomItem(Item):
    """RoomItems are items that fit inside rooms."""
    weight: int
    size: SizeCategory
