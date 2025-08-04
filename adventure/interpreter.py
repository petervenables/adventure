"""Interpreter class for the adventure game."""

import importlib
from typing import Any
from adventure.commands.command import Command
from adventure.statement import Statement
from adventure.exceptions import BadStatementError, CommandNotFoundError
from adventure.dao.doc_yaml import get_yaml_doc


class Interpreter:
    """Interpreter class handles both commands and statements."""

    def __init__(self):
        self.commands: list[Command] = self.get_commands()
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

    def get_commands(self) -> list[Command]:
        """Retrieve the command definitions from configuration."""

        cmd_dict: dict[str, Any] = get_yaml_doc("adventure/data/commands.yml")
        cmd_list: list[Command] = []
        for cmd in cmd_dict:
            action_func = None
            action_path = cmd.get("action")
            if action_path:
                # Dynamically import the action function based on the path
                module_path, func_name = action_path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                action_func = getattr(module, func_name, None)
                if not action_func:
                    raise ImportError(
                        f"Action function '{func_name}' not found in module '{module_path}'"
                    )
            new_cmd = Command(
                name=cmd.get("name"),
                desc=cmd.get("desc"),
                help_text=cmd.get("help"),
                action=action_func,
                aliases=cmd.get("aliases"),
            )
            cmd_list.append(new_cmd)
        return cmd_list
