"""adventure/command -- a command interpreter class to manage actions the player will attempt."""

import importlib
from typing import Union
from collections.abc import Callable
from adventure.exceptions import CommandNotFoundError


class Command:
    """A command class for individual verbs the player can perform."""

    def __init__(
        self,
        name: str,
        desc: str,
        help_text: str,
        aliases: list[str],
        action_path: str = None,
    ) -> None:
        self.name = name
        self.desc = desc
        self.help_text = help_text
        self.aliases: list[str] = aliases or []
        self.action_path = action_path
        self.action = self._import_action(self.action_path)

    def __str__(self):
        return f"{self.name} - {self.desc}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Command):
            return self.name.lower() == other.name.lower()
        raise ValueError("Comparable must be a Command object.")

    def _import_action(self, action_path: str) -> Callable:
        """Dynamically import the action function based on the path."""
        if not action_path:
            raise ValueError("Action path must be defined!")
        try:
            module_path, func_name = action_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            action_func = getattr(module, func_name, None)
            if not action_func:
                raise CommandNotFoundError(
                    f"Action '{func_name}' not found in module '{module_path}'"
                )
            return action_func
        except ImportError as e:
            raise ImportError(
                f"Error importing action for command '{self.name}': {e}"
            ) from e

    def do_action(self, game, *args, **kwargs) -> Union[str, None]:
        """Perform the action associated with this command."""
        return self.action(game, *args, **kwargs)
