"""The prompt class is for handling messages sent to the player."""

from typing import Dict
from dataclasses import dataclass, field
import yaml
from adventure.ui.baseui import BaseUI


@dataclass
class Prompt:
    """Prompt class defines messages given to the user."""

    msg: Dict = field(default_factory=dict)
    ui: BaseUI = None

    def load(self):
        """load the prompts from the YAML source."""
        stream = open("adventure/data/messages/prompts.yml", "r", encoding="UTF-8")
        self.msg = yaml.safe_load(stream)

    def read_input(self):
        """Read text-based commands from the user."""
        try:
            return self.ui.get_input("> ")
        except SystemExit as exc:
            raise SystemExit from exc

    def display(self, message: str, color: str = None):
        """Report a message to the user."""
        if self.ui:
            self.ui.display_message(message=message, color=color)
        else:
            print(message)

    def show(self, prompt_name: str, color: str = None):
        """Display a prompt to the user."""
        message = self.msg.get(prompt_name)
        self.display(message, color)

    def prepare(self, prompt_name: str, color: str = None):
        """Prepare a prompt for display."""
        message = self.msg.get(prompt_name)
        if not message:
            raise ValueError(f"Prompt '{prompt_name}' not found.")
        return self.ui.show_color(message, color) if color else message
