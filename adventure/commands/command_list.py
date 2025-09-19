"""CommandList module for the adventure game."""

from typing import Iterator
from adventure.commands.command import Command
from adventure.exceptions import CommandNotFoundError
from adventure.dao.doc_yaml import get_yaml_doc


class CommandList:
    """A class to manage a list of commands."""

    def __init__(self, commands_yml_file: str = None):
        self.commands: list[Command] = []
        if commands_yml_file:
            cmd_dict = get_yaml_doc(commands_yml_file)
            for cmd in cmd_dict:
                new_cmd = Command(
                    name=cmd.get("name"),
                    desc=cmd.get("desc"),
                    help_text=cmd.get("help_text"),
                    aliases=cmd.get("aliases", []),
                    action_path=cmd.get("action"),
                )
                self.commands.append(new_cmd)

    def __iter__(self) -> Iterator[Command]:
        """Allow iteration over the commands."""
        return iter(self.commands)

    def add_command(self, command: Command) -> None:
        """Add a command to the list."""
        self.commands.append(command)

    def get_command(self, name: str) -> Command:
        """Retrieve a command by name or alias."""
        for cmd in self.commands:
            if cmd.name.lower() == name.lower() or name.lower() in [
                alias.lower() for alias in cmd.aliases
            ]:
                return cmd
        raise CommandNotFoundError(f"Command '{name}' not found")

    def list_commands(self) -> list[str]:
        """List all available commands."""
        return [cmd.name for cmd in self.commands]

    def has_command(self, name: str) -> bool:
        """Check if a command exists by name or alias."""
        try:
            self.get_command(name)
            return True
        except CommandNotFoundError:
            return False
