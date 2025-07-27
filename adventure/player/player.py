"""Player class for the adventure game."""

from dataclasses import dataclass

from adventure.inventory import Inventory, Hands


@dataclass(kw_only=True)
class Player:
    """The player character in the adventure game."""

    name: str = "Player"
    description: str = "You look just like you always have."
    inventory: Inventory = Inventory()

    def __post_init__(self):
        """Initialize the player's inventory with hands."""
        self.inventory.add_container(Hands(), quiet=True)

    def __str__(self):
        return f"{self.name} - {self.description}"

    def look(self) -> str:
        """Return a description of the player."""
        return self.description

    def examine(self) -> str:
        """Return a detailed description of the player."""
        return f"You examine yourself closely: {self.description}"
