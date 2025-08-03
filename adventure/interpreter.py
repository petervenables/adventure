"""Interpreter class for the adventure game."""

from adventure.commands.command import Command
from adventure.statement import Statement
from adventure.exceptions import BadStatementError, CommandNotFoundError


class Interpreter:
    """Interpreter class handles both commands and statements."""

    def __init__(self, cmd_list: list[Command]):
        self.commands = cmd_list
        self.statements = []

    def identify_verb(self, statement: Statement) -> Command:
        """Match an input statement to an available command."""
        for token in statement.tokens:
            for cmd in self.commands:
                if token.lower() == cmd:
                    return cmd
                elif len(cmd.aliases) > 0:
                    if token.lower() in cmd.aliases:
                        return cmd
        raise CommandNotFoundError("Verb unknown")

    def prepare(self, stmt: str) -> Statement:
        """Intake a statement and make it ready for interpretation."""
        try:
            statement = Statement(stmt)
            statement.verb = self.identify_verb(statement)
            statement.args = statement.identify_args()
            self.statements.append(statement)
            return statement
        except BadStatementError as bse:
            raise bse
        except CommandNotFoundError as cnfe:
            raise cnfe
