"""adventure/item -- a class to handle things the player can pick up, move, or otherwise interact with."""

from dataclasses import dataclass


@dataclass(kw_only=True)
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

    def look(self) -> str:
        """Return a description of the item."""
        return self.long_desc

    def examine(self) -> str:
        """Return a detailed description of the item."""
        return f"You examine the {self.name} closely: {self.long_desc}"


@dataclass(kw_only=True)
class HandheldItem(Item):
    """A handheld item is one that can be carried in the player's hands."""

    weight: float
    bulk: int

    def show(self) -> str:
        """Show the item."""
        return f"You hold {self.name} out in front of you."

    def drop(self) -> str:
        """Drop the item."""
        return f"You drop {self.name} on the ground."


@dataclass(kw_only=True)
class ThrowableItem(HandheldItem):
    """A throwable item is one that can be thrown by the player."""

    def throw(self, target: str) -> bool:
        """Throw the item."""
        print(f"You throw {self.name}.")
        # Implement throwing logic here, e.g., affecting the game state or environment.
        # create_event("throw", self.name, target)
        # create_event("remove", self.name, target)
        # remove_from_inventory = True  # Placeholder for logic to remove the item from inventory.
        self.set_location(target)
        return True

    def set_location(self, location: str):
        """Set the location of the item."""
        # Placeholder for logic to set the item's location.
        print(f"The {self.name} is now at {location}.")
        # This would typically update the game's state to reflect the new location of the item.
