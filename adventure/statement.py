from adventure.commands.command import Command


class Statement:
    """A statement class to process the statements given by the player."""

    def __init__(self, statement: str):
        self.stmt = statement
        self.tokens: list[str] = statement.split()
        self.verb: Command
        self.args: list[str]

    def identify_args(self) -> list[str]:
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
