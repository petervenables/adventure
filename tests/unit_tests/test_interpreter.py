"""Test cases for the interpreter module."""

import pytest

from adventure.exceptions import CommandNotFoundError, BadStatementError
from adventure.interpreter import Interpreter
from adventure.commands.command import Command
from adventure.commands.command_list import CommandList

TEST_DIR = "tests/data"
TEST_COMMANDS_FILE = "test_commands.yml"


class TestInterpreter:
    """Test cases for the Interpreter class."""

    @pytest.fixture(autouse=True)
    def interpreter(self):
        """Fixture to create an Interpreter instance."""
        return Interpreter(commands_file=f"{TEST_DIR}/{TEST_COMMANDS_FILE}")

    def test_identify_verb_known_command(self, interpreter: Interpreter):
        """Test identifying a known command."""
        statement = "move west"
        stmt_obj = interpreter.prepare(statement)
        assert stmt_obj.verb.name == "move"

    @pytest.mark.parametrize(
        "statement,expected_verb",
        [
            ("go west", "move"),
            ("walk north", "move"),
            ("run east", "move"),
            ("take sword", "pick"),
            ("grab shield", "pick"),
            ("get potion", "pick"),
        ],
    )
    def test_command_alias_resolution(
        self, interpreter: Interpreter, statement: str, expected_verb: str
    ):
        """Test that command aliases are resolved correctly."""
        stmt_obj = interpreter.prepare(statement)
        assert stmt_obj.verb.name == expected_verb

    def test_identify_verb_unknown_command(self, interpreter: Interpreter):
        """Test handling of an unknown command."""
        statement = "unknowncmd arg1 arg2"
        with pytest.raises(CommandNotFoundError):
            interpreter.prepare(statement)

    def test_prepare_bad_statement(self, interpreter: Interpreter):
        """Test handling of a bad statement."""
        statement = ""
        with pytest.raises(BadStatementError):
            interpreter.prepare(statement)

    def test_get_commands(self, interpreter: Interpreter):
        """Test retrieval of commands from configuration."""
        assert isinstance(interpreter.commands, CommandList)
        for cmd in interpreter.commands:
            assert isinstance(cmd, Command)
