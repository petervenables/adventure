"""adventure/item -- a class to handle things the player can pick up, move, or otherwise interact with."""

from dataclasses import dataclass


@dataclass(kw_only=True)
class Item:
    """Items are the nonliving things we encounter in the adventure."""

    name: str
    aliases: list[str] = None
    short_desc: str
    long_desc: str

    def __str__(self):
        return f"{self.name} - {self.short_desc}"

    def __eq__(self, name: str) -> bool:
        if name in [self.name, *(self.aliases or [])]:
            return True
        return False

    def aka(self) -> list[str]:
        """Return a string listing the item's aliases."""
        if not self.aliases:
            return [self.name]
        return [self.name] + self.aliases

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


class LightSourceItem(Item):
    """A non-handheld light source item is one that can provide light in dark areas."""

    is_on: bool = False

    def is_lit(self) -> bool:
        """Return True if the light source is on, False otherwise."""
        return self.is_on

    def player_turn_on(self) -> str:
        """Turn on the light source."""
        if not self.is_on:
            self.is_on = True
            return f"You turn on the {self.name}."
        return f"The {self.name} is already on."

    def player_turn_off(self) -> str:
        """Turn off the light source."""
        if self.is_on:
            self.is_on = False
            return f"You turn off the {self.name}."
        return f"The {self.name} is already off."

    def env_turn_on(self) -> str:
        """Environment turns on the light source."""
        if not self.is_on:
            self.is_on = True
            return f"The {self.name} lights up."
        return f"The {self.name} is already on."

    def env_turn_off(self) -> str:
        """Environment turns off the light source."""
        if self.is_on:
            self.is_on = False
            return f"The {self.name} goes dark."
        return f"The {self.name} is already off."


class PullableItem(Item):
    """A pullable item is one that can be pulled by the player."""

    def pull(self) -> str:
        """Pull the item."""
        return f"You pull the {self.name}."


class SwitchItem(Item):
    """A switch is a control for an item that can be toggled on or off."""

    target: Item = None

    def set_target(self, target: Item):
        """Set the target item that this switch controls."""
        self.target = target

    def toggle(self) -> str:
        """Toggle the switch, affecting the target item."""
        if self.target is None:
            return f"You toggle the {self.name}, but nothing happens."
        if isinstance(self.target, LightSourceItem):
            if self.target.is_lit():
                return self.target.player_turn_off()
            else:
                return self.target.player_turn_on()
        # If it is some other kind of Item, implement other toggle logic here.
        return f"Toggling the {self.name} has no effect (yet)."
