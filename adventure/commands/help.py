"""Display the available commands to the player in the game."""


def help(self, *args, **kwargs):
    """Display the available commands."""
    output = "Available commands:\n"
    for cmd in self.interpreter.commands:
        output += f"{cmd.name}: {cmd.help_text}"
        output += "Type 'help <command>' for more information on a specific command."
    return output
