"""Tests for the statement module."""

import pytest
from adventure.statement import Statement
from adventure.exceptions import BadStatementError, CommandNotFoundError
from adventure.commands.command_list import CommandList

TEST_DATA_DIR = "tests/data"
TEST_COMMANDS = f"{TEST_DATA_DIR}/test_commands.yml"


class TestStatement:
    """Test Statement class."""

    def test_no_statement_raises(self):
        """Test that no statement raises BadStatementError."""
        with pytest.raises(BadStatementError):
            Statement(statement=None, cmd_list=None)

    def test_empty_statement_raises(self):
        """Test that empty statement raises BadStatementError."""
        with pytest.raises(BadStatementError):
            Statement(statement="", cmd_list=None)

    def test_statement_with_no_command_list_raises(self):
        """Test that statement with no command list raises CommandNotFoundError."""
        with pytest.raises(CommandNotFoundError):
            Statement(statement="look", cmd_list=None)

    def test_statement_with_unknown_command_raises(self):
        """Test that statement with unknown command raises CommandNotFoundError."""
        with pytest.raises(CommandNotFoundError):
            Statement(statement="unknowncmd arg1 arg2", cmd_list=[])

    def test_statement_with_known_command(self):
        """Test that statement with known command works."""
        cmd_list = CommandList(commands_yml_file=TEST_COMMANDS)
        stmt = Statement(statement="look around", cmd_list=cmd_list)
        assert stmt.verb.name == "look"
        assert stmt.args == ["around"]

    def test_statement_with_empty_statement(self):
        """Test that statement with empty statement raises BadStatementError."""
        cmd_list = CommandList(commands_yml_file=TEST_COMMANDS)
        with pytest.raises(BadStatementError):
            Statement.identify_verb(Statement, tokens=[], commands=cmd_list)
