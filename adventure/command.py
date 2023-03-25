"""adventure/command -- a command interpreter class to manage actions the player will attempt."""
from typing import List
from adventure.exceptions import BadStatementError, CommandNotFoundError

class Command:
    """A command class for individual verbs the player can perform."""
    def __init__(self, name: str, desc: str, aliases: List[str], action: callable):
        self.name = name
        self.desc = desc
        self.aliases: List[str] = aliases or []
        self.action = action

    def __str__(self):
        return f"{self.name} - {self.desc}"

    def __eq__(self, name: str) -> bool:
        # might want to make this based on regex so 'm' can be 'move'
        if name == self.name:
            return True
        return False

    def do_action(self, *args, **kwargs):
        """Perform the action associated with this command."""
        return self.action(*args, **kwargs)

class Statement:
    """A statement class to process the statements given by the player."""
    def __init__(self, statement: str):
        self.stmt = statement
        self.tokens: List[str] = statement.split()
        self.verb: Command
        self.args: List[str]

    def identify_args(self) -> List[str]:
        """Separate the args from the verb in the statement."""
        self.args = self.tokens
        if self.verb is not None:
            if self.verb.name in self.args:
                self.args.remove(self.verb.name)
            else:
                for alias in self.verb.aliases:
                    if alias in self.args:
                        self.args.remove(alias)
        return self.args

class Interpreter:
    """Interpreter class handles both commands and statements."""

    def __init__(self, cmd_list: List[Command]):
        self.commands = cmd_list
        self.statements = []

    def identify_verb(self, statement: Statement)-> Command:
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
