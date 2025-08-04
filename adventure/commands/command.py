"""adventure/command -- a command interpreter class to manage actions the player will attempt."""

from typing import Union
from collections.abc import Callable


class Command:
    """A command class for individual verbs the player can perform."""

    def __init__(
        self,
        name: str,
        desc: str,
        help_text: str,
        aliases: list[str],
        action: Callable = None,
    ) -> None:
        self.name = name
        self.desc = desc
        self.help_text = help_text
        self.aliases: list[str] = aliases or []
        self.action = action

    def __str__(self):
        return f"{self.name} - {self.desc}"

    def __eq__(self, name: str) -> bool:
        # might want to make this based on regex so 'm' can be 'move'
        if name.lower() == self.name.lower():
            return True
        return False

    def set_action(self, action: Callable):
        """Set the action for this command."""
        self.action = action

    def do_action(self, game, *args, **kwargs) -> Union[str, None]:
        """Perform the action associated with this command."""
        return self.action(game, *args, **kwargs)
