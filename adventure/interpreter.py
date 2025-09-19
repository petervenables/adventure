"""Interpreter class for the adventure game."""

from adventure.commands.command import Command
from adventure.commands.command_list import CommandList
from adventure.statement import Statement
from adventure.exceptions import BadStatementError, CommandNotFoundError

from adventure.defaults import DEFAULT_COMMANDS_FILE


class Interpreter:
    """Interpreter class handles both commands and statements."""

    def __init__(self, commands_file: str = DEFAULT_COMMANDS_FILE):
        self.commands: CommandList = CommandList(commands_file)
        self.statements = []

    def prepare(self, stmt: str) -> Statement:
        """Intake a statement and make it ready for interpretation."""
        try:
            statement = Statement(stmt, self.commands)
            # statement.verb = self.identify_verb(statement)
            # statement.args = statement.identify_args()
            # self.statements.append(statement)
            return statement
        except BadStatementError as e:
            raise BadStatementError from e
        except CommandNotFoundError as e:
            raise CommandNotFoundError from e
