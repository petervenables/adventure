"""Statement processing for the adventure game."""

from typing import Union
from adventure.commands.command import Command
from adventure.commands.command_list import CommandList
from adventure.exceptions import BadStatementError, CommandNotFoundError


class Statement:
    """A statement class to process the statements given by the player."""

    def __init__(self, statement: str = None, cmd_list: CommandList = None) -> None:
        if not statement:
            raise BadStatementError("No statement given")
        self.stmt = statement
        self.action: str = ""
        self.tokens: list[str] = statement.split()
        try:
            self.verb: Command = self.identify_verb(self.tokens, cmd_list)
        except CommandNotFoundError as e:
            raise CommandNotFoundError from e
        if not self.verb:
            raise CommandNotFoundError("No valid command found.")
        # self.object: list[str] = self.identify_objects(self.tokens)
        # self.mods: list[str] = self.identify_modifiers(self.tokens)
        # Probably deprecated
        self.args: list[str] = self.identify_args()

    def identify_verb(
        self, tokens: list[str], commands: CommandList
    ) -> Union[Command, None]:
        """Identify the verb in the statement.

        Args:
            tokens (list[str]): The list of tokens from the statement.
            commands (list[str]): The list of available command names and aliases.

        Returns:
            Union[str, None]: The token with a valid command name or
                None if not found.

        """
        if not tokens:
            raise BadStatementError("No tokens to identify verb from")
        if not commands:
            raise CommandNotFoundError("No commands available to match verb")
        for token in tokens:
            for command in commands:
                if token == command.name or token in command.aliases:
                    self.action = token
                    return command
        return None

    def identify_args(self) -> list[str]:
        """Separate the args from the verb in the statement."""
        self.args = [token for token in self.tokens if token != self.action]
        return self.args
