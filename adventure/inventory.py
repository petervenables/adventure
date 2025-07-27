"""adventure/inventory -- what you have in your hands, pockets, and bags."""

from dataclasses import dataclass
from typing import Dict, List
from colorama import Fore, Style
from adventure.items.item import Item
from adventure.exceptions import (
    ItemNotFoundError,
    ContainerNotFoundError,
    ContainerCannotFitError,
    ContainerFullError,
    DuplicateContainerError,
)


@dataclass
class Container:
    name: str
    short_desc: str
    capacity: int
    contents: List[Item]

    def get(self, name) -> Item:
        for item in self.contents:
            if name == item.name:
                return item
        raise ItemNotFoundError(f"Could not find an item named {name} in {self.name}.")

    def check_bulk(self) -> int:
        sum_bulk: int = 0
        for item in self.contents:
            sum_bulk += item.bulk
        return sum_bulk

    def is_empty(self) -> bool:
        if len(self.contents) == 0:
            return True
        return False

    def is_full(self) -> bool:
        if self.check_bulk() >= self.capacity:
            return True
        return False

    def can_fit(self, item: Item) -> bool:
        if self.check_bulk() + item.bulk <= self.capacity:
            return True
        return False

    def insert(self, item: Item):
        if self.is_full():
            raise ContainerFullError(f"{self.name} is full. Cannot insert {item.name}.")
        if not self.can_fit(item):
            raise ContainerCannotFitError(
                f"{item.name} is too large to fit in {self.name}."
            )
        self.contents.append(item)

    def remove(self, item: Item) -> Item:
        """Remove a named item from a container.

        Arguments:
         - item(Item):      The item to remove.

        Returns:
         - (Item):          The Item so named in the container.

        Raises:
         - (ItemNotFoundError): If the named item is not in the container.

        """
        try:
            self.contents.remove(item)
            return item
        except Exception as excp:
            raise ItemNotFoundError from excp


class Hands(Container):
    """A special container for the player's hands."""

    def __init__(self):
        super().__init__(name="hands", short_desc="your hands", capacity=2, contents=[])

    def __str__(self):
        return f"{self.name} - {self.short_desc} (capacity: {self.capacity})"

    def in_right_hand(self) -> str:
        """Return a description of what is in the right hand."""
        if len(self.contents) > 0:
            if self.is_full():
                return f"You are holding {self.contents[0].name} in both hands."
            return f"You are holding {self.contents[0].name} in your right hand."
        return "Your right hand is empty."

    def in_left_hand(self) -> str:
        """Return a description of what is in the left hand."""
        if len(self.contents) > 0:
            if self.is_full():
                return f"You are holding {self.contents[0].name} in both hands."
            return f"You are holding {self.contents[1].name} in your left hand."
        return "Your left hand is empty."

    def drop_right(self) -> str:
        """Drop the item in the right hand."""
        if len(self.contents) > 0:
            if len(self.contents) == 1 and self.is_full():
                item = self.contents[0]
                self.remove(item)
                return f"You drop {item.name} from both hands."
            item = self.contents[0]
            self.remove(item)
            return f"You drop {item.name} from your right hand."
        return "Your right hand is empty."

    def drop_left(self) -> str:
        """Drop the item in the left hand."""
        if len(self.contents) == 1 and self.is_full():
            item = self.contents[0]
            self.remove(item)
            return f"You drop {item.name} from both hands."
        if len(self.contents) > 1:
            item = self.contents[1]
            self.remove(item)
            return f"You drop {item.name} from your left hand."
        return "Your left hand is empty."

    def insert_right(self, item: Item) -> str:
        """Insert an item into the right hand."""
        if self.can_fit(item):
            self.insert(item)
            return f"You insert {item.name} into your right hand."
        return "Your hands are full. You cannot hold more than two items."

    def insert_left(self, item: Item) -> str:
        """Insert an item into the left hand."""
        if self.can_fit(item):
            self.insert(item)
            return f"You insert {item.name} into your left hand."
        return "Your hands are full. You cannot hold more than two items."


class Inventory:
    """Defines the things that can hold things for the player."""

    containers: List[Container] = []

    def get(self, name: str) -> Container:
        """Retrieve a named container from the Inventory.

        Arguments:
         - name(str):       The name of the container to retrieve.

        Returns:
         - (Container):     The container so named if it exists.

        Raises:
         - (ContainerNotFoundError): If the container is not in the player's possession.

        """
        for container in self.containers:
            if name == container.name:
                return container
        raise ContainerNotFoundError(f"No container named {name} on your person.")

    def add_container(self, container: Container, quiet: bool):
        """Add a container object to the inventory."""
        try:
            self.get(container.name)
            raise DuplicateContainerError(
                f"You cannot have more than one {container.name}."
            )
        except ContainerNotFoundError:
            if not quiet:
                print(Fore.CYAN + f"You add a {container.name} to your inventory.")
            self.containers.append(container)

    def remove_container(self, name: str) -> Container:
        """Removes a container from the player's possession and returns it to be put in the room.

        Arguments:
          - name(str):      the name of the container to remove.

        Returns:
          - (Container):    the container so identified by name.

        Raises:
          - (ContainerNotFoundError): if the container is not in the player's possession.

        """
        try:
            container = self.get(name)
            return container
        except ContainerNotFoundError as cnfe:
            raise cnfe

    def list_contents(self, container_name: str):
        """Print out what's in a named container."""
        output = ""
        for container in self.containers:
            if container_name == container.name:
                if container.is_empty():
                    output += "Nothing\n"
                else:
                    for item in container.contents:
                        output += f"{item}\n"
        return output

    def list_all_contents(self):
        """Print out what's in all containers."""
        output = ""
        for container in self.containers:
            output += f"In {container.short_desc}:\n"
            output += self.list_contents(container.name)
        return output

    def list_all_containers(self) -> List:
        """Get a list of all container names."""
        names = []
        for container in self.containers:
            names.append(container.name)
        return names

    def can_hold(self, name: str, item: Item) -> bool:
        """Check if the inventory can hold an item in a named container.

        Arguments:
         - name(str):       The name of the container to check.
         - item(Item):      the Item we want to store.

        Returns:
         - (bool):          True if the item will fit, False otherwise.

        """
        try:
            container = self.get(name)
            if container.can_fit(item):
                return True
            else:
                print(
                    Fore.LIGHTRED_EX
                    + f"You cannot fit {item.name} in {container.name} right now."
                    + Style.RESET_ALL
                )
                return False
        except ContainerNotFoundError:
            print(
                Fore.LIGHTRED_EX
                + f"You seem to be unable to locate {container.short_desc}"
                + Style.RESET_ALL
            )
            return False

    def insert_into(self, dest: str, item: Item) -> bool:
        """Put an item into a specific container.

        Arguments:
         - dest(str):       The name of the container to put the item into.
         - item(Item):      The Item to insert.

        Returns:
         - (bool):          True if the insert was done, False otherwise.
        """
        try:
            container = self.get(dest)
            if container.can_fit(item):
                container.insert(item)
                return True
            print(
                Fore.LIGHTRED_EX
                + f"You can't seem to fit {item.name} into {container.name}"
                + Style.RESET_ALL
            )
            return False
        except ContainerNotFoundError:
            print(
                Fore.LIGHTRED_EX
                + f"You seem to be unable to locate {container.short_desc}"
                + Style.RESET_ALL
            )
            return False

    def swap_container_item(self, source: str, dest: str, item_name: str) -> bool:
        """Move an item from one container to another.

        Arguments:
         - source(str):         The origin container from which to take the item.
         - dest(str):           The destination container to which to move the item.
         - item_name(str):      The name of the item to move.

        Returns:
         - (bool)               True if the swap was done, False, otherwise.
        """
        try:
            src_container = self.get(source)
            dst_container = self.get(dest)
            item = src_container.get(item_name)
            if dst_container.can_fit(item):
                src_container.remove(item)
                dst_container.insert(item)
                return True
            print(
                Fore.LIGHTRED_EX
                + f"You can't seem to fit {item.name} into {dst_container.name}"
                + Style.RESET_ALL
            )
            return False
        except ItemNotFoundError:
            print(
                Fore.LIGHTRED_EX
                + f"There's no {item_name} in {src_container.name}."
                + Style.RESET_ALL
            )
        except ContainerNotFoundError as cnfe:
            print(Fore.LIGHTRED_EX + f" {cnfe} " + Style.RESET_ALL)

    def find_item(self, item_name: str) -> List[Dict[str, Item]]:
        """Search through all containers to find a named item."""
        found = []
        for container in self.containers:
            for item in container.contents:
                if item_name == item.name:
                    found.append({"where": container.name, "what": item})
        if len(found) > 0:
            return found
        raise ItemNotFoundError(f"Item {item_name} not found in any container.")

    def holding(self, item_name: str) -> bool:
        """Check if the player is holding a named item."""
        for container in self.containers:
            for item in container.contents:
                if item_name == item.name:
                    return True
        return False
