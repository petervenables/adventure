"""adventure/game -- track the game state and history."""

from typing import Any, Union
from textwrap import wrap
from colorama import Fore, Style
from adventure.rooms.room import Room
from adventure.commands.command import Command
from adventure.interpreter import Interpreter
from adventure.constants import self_words, visibility_mod_words, mobility_mod_words
from adventure.exceptions import ContainerNotFoundError, ItemNotFoundError
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.action.item_swap import item_swap
from adventure.map.map import Map
from adventure.player.player import Player


class Game:
    """This is the game class."""

    is_running: bool
    current_loc: Room = None
    interpreter: Interpreter
    map: Map = Map()
    player: Player = Player()

    def __init__(self):
        self.is_running = True
        self.interpreter = Interpreter(cmd_list=get_commands(self))
        self.map.load_yaml("adventure/data/maps/start_map.yml")
        self.current_loc = self.map.get_room(0)

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
                    return (
                        Fore.GREEN
                        + "You've certainly looked better but you're not bad."
                        + Style.RESET_ALL
                    )
                found = []
                try:
                    # Look for a describable item in the room
                    for each in self.current_loc.in_room(thing_name):
                        found.append(each)
                except ItemNotFoundError:
                    # if not in the room, perhaps we have it on hand?
                    try:
                        for each in self.player.inventory.find_item(thing_name):
                            found.append(each)
                    except ItemNotFoundError:
                        return (
                            Fore.GREEN
                            + f"You don't see {thing_name} here."
                            + Style.RESET_ALL
                        )
                if len(found) > 0:
                    for item in found:
                        return (
                            Fore.BLUE
                            + f"It is {item['what'].short_desc} ({item['where']})"
                            + Style.RESET_ALL
                        )
            else:
                # look around the room
                output = ""
                for line in wrap(self.current_loc.long_desc, width=80):
                    output += Fore.GREEN + line + Style.RESET_ALL + "\n"
                output += (
                    Fore.LIGHTMAGENTA_EX
                    + "\nDoors: "
                    + self.current_loc.show_doors()
                    + Style.RESET_ALL
                )
                return output

    def search(self, *args, **kwargs):
        """Search the room for items."""
        output = "An exhaustive search of the room reveals the following items:\n"
        if len(self.current_loc.contents) == 0:
            output += Fore.LIGHTGREEN_EX + "*nothing*" + Style.RESET_ALL
        else:
            for item in self.current_loc.contents:
                output += Fore.LIGHTGREEN_EX + f"*{item.name}*" + Style.RESET_ALL
        return output

    def move(self, *args, **kwargs):
        """Move the player around the map."""
        if len(args[0]) == 0:
            return Fore.GREEN + "You wander about the room." + Style.RESET_ALL
        else:
            for word in args[0]:
                if word in mobility_mod_words:
                    args[0].remove(word)
            if len(args[0]) == 0:
                return Fore.GREEN + "You wander about the room." + Style.RESET_ALL
            direction = args[0].pop()
            for wall in self.current_loc.get_doors():
                if direction.lower() == wall.location.name.lower():
                    for door in wall.doors:
                        if door.is_open and not door.is_blocked:
                            if door.leads_to is not None:
                                self.current_loc = self.map.get_room(door.leads_to)
                                return (
                                    Fore.GREEN
                                    + f"You walk through the {door.name} to {self.current_loc.name}."
                                    + Style.RESET_ALL
                                )
                            else:
                                return (
                                    Fore.LIGHTRED_EX
                                    + "You can't go that way."
                                    + Style.RESET_ALL
                                )
                    return (
                        Fore.BLUE
                        + "You attempt to walk in that direction but are stopped by an invisible force."
                        + Style.RESET_ALL
                    )
            return (
                Fore.GREEN + "You don't see how you can go that way." + Style.RESET_ALL
            )

    def pick(self, *args, **kwargs):
        """Obtain an item from the room."""
        if len(args) > 0:
            if len(args[0]) == 0:
                return Fore.GREEN + "You pick your nose, briefly."
            else:
                if "up" in args[0]:
                    args[0].remove("up")
                for item in self.current_loc.contents:
                    if item.name.lower() in args[0]:
                        if item.weight <= 100:
                            if self.player.inventory.can_hold("hands", item):
                                self.player.inventory.insert_into("hands", item)
                                self.current_loc.contents.remove(item)
                                return (
                                    Fore.LIGHTMAGENTA_EX
                                    + f"You pick up {item.name}."
                                    + Style.RESET_ALL
                                )
                            else:
                                return (
                                    Fore.LIGHTRED_EX
                                    + "You don't have a free hand to pick that up."
                                    + Style.RESET_ALL
                                )
                        else:  # If the item is too heavy
                            return (
                                Fore.LIGHTRED_EX
                                + f"The {item.name} is too heavy for you to pick up."
                                + Style.RESET_ALL
                            )
                return Fore.LIGHTRED_EX + "You don't see that here." + Style.RESET_ALL

    def drop(self, *args, **kwargs):
        """Drop an item from inventory to the room."""
        if len(args[0]) == 0:
            return Fore.GREEN + "You drop nothing like a bad habit." + Style.RESET_ALL
        else:
            if "all" in args[0]:
                # We'll interpret this as dropping what we're holding, not all bags.
                output = ""
                try:
                    hands = self.player.inventory.get("hands")
                    if not hands.is_empty():
                        output += "You dropped:\n"
                        for item in hands.contents:
                            hands.contents.remove(item)
                            self.current_loc.contents.append(item)
                            output += Fore.GREEN + f"*{item.name}*\n" + Style.RESET_ALL
                except ContainerNotFoundError:
                    # We'll assume they know they're missing a hand if they are...
                    return
                return output
            else:
                for item_name in args[0]:
                    found = False
                    for container in self.player.inventory.containers:
                        try:
                            found = container.get(item_name)
                            container.remove(found)
                            self.current_loc.contents.append(found)
                            output = "You dropped:\n"
                            output += (
                                Fore.LIGHTMAGENTA_EX
                                + f"*{found.name}* from {container.short_desc}."
                                + Style.RESET_ALL
                            )
                            return output
                        except ItemNotFoundError:
                            continue
                    if found is False:
                        return (
                            Fore.LIGHTRED_EX
                            + f"You couldn't find {item_name} to drop."
                            + Style.RESET_ALL
                        )

    def throw(self, *args, **kwargs) -> Union[str | None]:
        """Throw an item from inventory to the room."""
        thrown_thing = None
        target = None
        if len(args[0]) == 0:
            return (
                Fore.GREEN + "You throw your hands out into the air." + Style.RESET_ALL
            )
        else:
            thrown_thing = args[0].pop(0)
            if not self.player.inventory.holding(thrown_thing):
                return (
                    Fore.LIGHTRED_EX
                    + f"You don't have {thrown_thing} to throw."
                    + Style.RESET_ALL
                )
            else:
                item_list = self.player.inventory.find_item(thrown_thing)
            if thrown_thing in self_words:
                return (
                    Fore.LIGHTRED_EX
                    + "You can't throw yourself, you silly goose."
                    + Style.RESET_ALL
                )
            if "at" in args[0]:
                target_name = args[0].pop(args[0].index("at") + 1)
                if target_name in self_words:
                    return (
                        Fore.LIGHTRED_EX
                        + f"You bounce {thrown_thing} off your own head."
                        + Style.RESET_ALL
                    )
                if target_name not in self.current_loc.contents:
                    return (
                        Fore.LIGHTRED_EX
                        + f"You can't throw {thrown_thing} at {target_name} because it isn't here."
                        + Style.RESET_ALL
                    )

            for found in item_list:
                container_name = found.get("where")
                item = found.get("what")
                container = self.player.inventory.get(container_name)
                container.remove(item)
                self.current_loc.contents.append(item)
                if target:
                    return (
                        Fore.LIGHTMAGENTA_EX
                        + f"You throw {found.get('what').name} from {container.short_desc} at {target_name}."
                        + Style.RESET_ALL
                    )
                else:
                    return (
                        Fore.LIGHTMAGENTA_EX
                        + f"You throw {found.get('what')} from {container.short_desc}."
                        + Style.RESET_ALL
                    )

    def inv(self, *args, **kwargs):
        """Display the things you have on hand."""
        print(self.player.inventory.list_all_contents())

    def swap(self, *args, **kwargs):
        """Swap an item from one container to another."""
        try:
            item_swap(*args, self.player.inventory)
        except ItemNotFoundError:
            return "You can't seem to locate that to swap it."

    def help(self, *args, **kwargs):
        """Display the available commands."""
        output = Fore.YELLOW + "Available commands:" + Style.RESET_ALL
        for cmd in self.interpreter.commands:
            output += Fore.CYAN + f"{cmd.name}: {cmd.help_text}" + Style.RESET_ALL
            output += (
                Fore.YELLOW
                + "Type 'help <command>' for more information on a specific command."
                + Style.RESET_ALL
            )
        return output


def get_commands(game: Game) -> list[Command]:
    """Retrieve the command definitions from configuration."""
    cmd_dict: dict[str, Any] = get_yaml_doc("adventure/data/commands.yml")
    cmd_list: list[Command] = []
    for cmd in cmd_dict:
        new_cmd = Command(
            name=cmd.get("name"),
            desc=cmd.get("desc"),
            help_text=cmd.get("help"),
            action=getattr(game, cmd.get("action")),
            aliases=cmd.get("aliases"),
        )
        cmd_list.append(new_cmd)
    return cmd_list
