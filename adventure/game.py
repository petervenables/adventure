"""adventure/game -- track the game state and history."""
from typing import List, Dict
from textwrap import wrap
from colorama import Fore, Style
from adventure.room import Room
from adventure.item import Item
from adventure.inventory import Inventory
from adventure.command import Interpreter, Command
from adventure.constants import self_words, visibility_mod_words, mobility_mod_words
from adventure.exceptions import ContainerNotFoundError, ItemNotFoundError
from adventure.setup import start_room, start_rock
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.action.item_swap import item_swap

class Game:
    """This is the game class."""
    is_running: bool
    current_loc: Room
    visited: List[Room] = []
    inventory: Inventory
    interpreter: Interpreter

    def __init__(self):
        self.is_running = True
        self.current_loc = start_room()
        self.current_loc.contents.append(start_rock())
        self.visited.append(self.current_loc)
        self.inventory = Inventory()
        self.interpreter = Interpreter(cmd_list=get_commands(self))

    def quit_game(self, *args, **kwargs):
        """We are LEAVING!"""
        self.is_running = False

    def look(self, *args, **kwargs):
        """Look at things held or in the room."""
        if len(args) > 0:
            for word in args[0]:
                if word in visibility_mod_words:
                    args[0].remove(word)
            if len(args[0]) > 0:
                thing_name = args[0].pop()
                if thing_name in self_words:
                    print(Fore.GREEN + "You've certainly looked better but you're not bad." + Style.RESET_ALL)
                    return
                found = []
                try:
                    # Look for a describable item in the room
                    for each in self.current_loc.in_room(thing_name):
                        found.append(each)
                except ItemNotFoundError:
                    # if not in the room, perhaps we have it on hand?
                    try:
                        for each in self.inventory.find_item(thing_name):
                            found.append(each)
                    except ItemNotFoundError:
                        print(Fore.GREEN + f"You don't see {thing_name} here." + Style.RESET_ALL)
                if len(found) > 0:
                    for item in found:
                        print(Fore.BLUE + f"It is {item['what'].short_desc} ({item['where']})" + Style.RESET_ALL)
            else:
                # look around the room
                for line in wrap(self.current_loc.long_desc, width=80):
                    print(Fore.GREEN + line + Style.RESET_ALL)
                print(Fore.LIGHTMAGENTA_EX + "Doors: " + self.current_loc.show_doors() + Style.RESET_ALL)

    def search(self, *args, **kwargs):
        """Search the room for items."""
        if len(self.current_loc.contents) > 0:
            print("An exhaustive search of the room reveals the following items:")
            for item in self.current_loc.contents:
                print(Fore.LIGHTGREEN_EX + f"*{item.name}*" + Style.RESET_ALL)
            if len(self.current_loc.contents) == 0:
                print(Fore.LIGHTGREEN_EX + "*nothing*" + Style.RESET_ALL)

    def move(self, *args, **kwargs):
        """Move the player around the map."""
        if len(args[0]) == 0:
            print(Fore.GREEN + "You wander about the room." + Style.RESET_ALL)
        else:
            for word in args[0]:
                if word in mobility_mod_words:
                    args[0].remove(word)
            if len(args[0]) == 0:
                print(Fore.GREEN + "You wander about the room." + Style.RESET_ALL)
            direction = args[0].pop()
            for wall in self.current_loc.get_doors():
                if direction.lower() == wall.location.name.lower():
                    print(Fore.BLUE + "You attempt to walk in that direction but are stopped by an invisible force." + Style.RESET_ALL)
                    return
            print(Fore.GREEN + "You don't see how you can go that way." + Style.RESET_ALL)
            return

    def pick(self, *args, **kwargs):
        """Obtain an item from the room."""
        if len(args) > 0:
            if len(args[0]) == 0:
                print(Fore.GREEN + "You pick your nose, briefly.")
            else:
                if "up" in args[0]:
                    args[0].remove("up")
                for item in self.current_loc.contents:
                    if item.name.lower() in args[0]:
                        if item.weight <= 100:
                            picked = None
                            if self.inventory.can_hold("right", item):
                                self.inventory.insert_into("right", item)
                                picked = "right"
                            elif self.inventory.can_hold("left", item):
                                self.inventory.insert_into("left", item)
                                picked = "left"
                            if picked:
                                print(Fore.LIGHTMAGENTA_EX + f"You pick up {item.name} with your {picked} hand." + Style.RESET_ALL)
                                self.current_loc.contents.remove(item)
                                return
                            else:
                                print(Fore.LIGHTRED_EX + "You don't have a free hand to pick that up." + Style.RESET_ALL)
                                return
                        elif item.weight > 100:
                            print(Fore.LIGHTRED_EX + f"The {item.name} is too heavy for you to pick up." + Style.RESET_ALL)
                            return
                print(Fore.LIGHTRED_EX + "You don't see that here." + Style.RESET_ALL)

    def drop(self, *args, **kwargs):
        """Drop an item from inventory to the room."""
        if len(args[0]) == 0:
            print(Fore.GREEN + "You drop nothing like a bad habit." + Style.RESET_ALL)
        else:
            if "all" in args[0]:
                for hand in ["left", "right"]:
                    # We'll interpret this as dropping what we're holding, not all bags.
                    try:
                        hand = self.inventory.get(hand)
                        if len(hand.contents) > 0:
                            for item in hand.contents:
                                hand.contents.remove(item)
                                self.current_loc.contents.append(item)
                                print(Fore.GREEN + f"From {hand.short_desc} you dropped {item.name}" + Style.RESET_ALL)
                    except ContainerNotFoundError:
                        # We'll assume they know they're missing a hand if they are...
                        return
                return
            else:
                for item_name in args[0]:
                    found = False
                    for container in self.inventory.containers:
                        try:
                            found = container.get(item_name)
                            container.remove(found)
                            self.current_loc.contents.append(found)
                            print(Fore.LIGHTMAGENTA_EX + f"You drop {found.name} from {container.short_desc}." + Style.RESET_ALL)
                            continue
                        except ItemNotFoundError:
                            continue
                    if found is False:
                        print(Fore.LIGHTRED_EX + f"You couldn't find {item_name} to drop." + Style.RESET_ALL)

    def inv(self, *args, **kwargs):
        """Display the things you have on hand."""
        self.inventory.list_all_contents()

    def swap(self, *args, **kwargs):
        """Swap an item from one container to another."""
        try:
            item_swap(*args, self.inventory)
        except ItemNotFoundError:
            print("You can't seem to locate that to swap it.")

def get_commands(game: Game) -> List[Command]:
    """Retrieve the command definitions from configuration."""
    cmd_dict: Dict = get_yaml_doc("adventure/data/commands.yml")
    cmd_list: List = []
    for cmd in cmd_dict:
        new_cmd = Command(
            name=cmd.get('name'),
            desc=cmd.get('desc'),
            action=getattr(game, cmd.get('action')),
            aliases=cmd.get('aliases')
        )
        cmd_list.append(new_cmd)
    return cmd_list
