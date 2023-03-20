"""adventure/inventory -- what you have in your hands, pockets, and bags."""
from dataclasses import dataclass
from typing import List
from colorama import Fore, Style
from adventure.item import Item
from adventure.exceptions import ItemNotFoundError, ContainerNotFoundError, DuplicateContainerError


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
            sum_bulk += item.size.bulk
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
        if self.check_bulk() + item.size.bulk <= self.capacity:
            return True
        return False

    def insert(self, item: Item):
        if self.can_fit(item):
            self.contents.append(item)

    def remove(self, name: str) -> Item:
        """Remove a named item from a container.
        
        Arguments:
         - name(str):       The name of the item to remove.

        Returns:
         - (Item):          The Item so named in the container.

        Raises:
         - (ItemNotFoundError): If the named item is not in the container.
        
        """
        try:
            found = self.get(name)
            self.contents.remove(found)
            return found
        except ItemNotFoundError as infe:
            raise infe

class Inventory:
    """Defines the things that can hold things for the player."""
    containers: List[Container] = []

    def __init__(self):
        right = Container(name="right", short_desc="your right hand", capacity=1, contents=[])
        left = Container(name="left", short_desc="your left hand", capacity=1, contents=[])
        self.add_container(right, quiet=True)
        self.add_container(left, quiet=True)

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
            raise DuplicateContainerError(f"You cannot have more than one {container.name}.")
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
        for container in self.containers:
            if container_name == container.name:
                if len(container.contents) == 0:
                    print(Fore.LIGHTRED_EX + "Nothing" + Style.RESET_ALL)
                for item in container.contents:
                    print(Fore.LIGHTBLUE_EX + f"{item}" + Style.RESET_ALL)

    def list_all_contents(self):
        for container in self.containers:
            print(Fore.LIGHTMAGENTA_EX + f"In {container.short_desc}:" + Style.RESET_ALL)
            self.list_contents(container.name)

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
                print(Fore.LIGHTRED_EX + f"You cannot fit {item.name} in {container.name} right now." + Style.RESET_ALL)
                return False
        except ContainerNotFoundError:
            print(Fore.LIGHTRED_EX + f"You seem to be unable to locate {container.short_desc}" + Style.RESET_ALL)
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
            print(Fore.LIGHTRED_EX + f"You can't seem to fit {item.name} into {container.name}" + Style.RESET_ALL)
            return False
        except ContainerNotFoundError:
            print(Fore.LIGHTRED_EX + f"You seem to be unable to locate {container.short_desc}" + Style.RESET_ALL)
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
            print(Fore.LIGHTRED_EX + f"You can't seem to fit {item.name} into {dst_container.name}" + Style.RESET_ALL)
            return False
        except ItemNotFoundError:
            print(Fore.LIGHTRED_EX + f"There's no {item_name} in {src_container.name}." + Style.RESET_ALL)
        except ContainerNotFoundError as cnfe:
            print(Fore.LIGHTRED_EX + f" {cnfe} " + Style.RESET_ALL)

    def find_item(self, item_name: str) -> List[Item]:
        """Search through all containers to find a named item."""
        found = []
        for container in self.containers:
            for item in container.contents:
                if item_name == item.name:
                    found.append(item)
        if len(found) > 0:
            return found
        raise ItemNotFoundError(f"Item {item_name} not found in any container.")
