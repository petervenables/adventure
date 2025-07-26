"""The prompt class is for handling messages sent to the player."""

from typing import Dict
from dataclasses import dataclass, field
import yaml
from colorama import init, Fore, Style


@dataclass
class Prompt:
    """Prompt class defines messages given to the user."""

    msg: Dict = field(default_factory=dict)

    def load(self):
        """load the prompts from the YAML source."""
        init()
        stream = open("adventure/data/messages/prompts.yml", "r", encoding="UTF-8")
        self.msg = yaml.safe_load(stream)

    def read_input(self):
        """Read text-based commands from the user."""
        return input("> ")

    def blue(self, prompt_name: str) -> str:
        """return a message from the prompts using blue text."""
        return Fore.BLUE + self.msg.get(prompt_name) + Style.RESET_ALL

    def red(self, prompt_name: str) -> str:
        """return a message from the prompts using red text."""
        return Fore.RED + self.msg.get(prompt_name) + Style.RESET_ALL

    def yellow(self, prompt_name: str) -> str:
        """return a message from the prompts using yellow text."""
        return Fore.YELLOW + self.msg.get(prompt_name) + Style.RESET_ALL

    def green(self, prompt_name: str) -> str:
        """return a message from the prompts using green text."""
        return Fore.GREEN + self.msg.get(prompt_name) + Style.RESET_ALL

    def magenta(self, prompt_name: str) -> str:
        """return a message from the prompts using magenta text."""
        return Fore.MAGENTA + self.msg.get(prompt_name) + Style.RESET_ALL
