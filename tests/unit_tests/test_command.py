"""Unit tests for the Command module."""

import pytest
from adventure.commands.command import Command
from adventure.exceptions import CommandNotFoundError


@pytest.fixture
def hop_cmd():
    cmd = Command(
        name="hop",
        desc="A sudden motion forward",
        help_text="For taking a playful movement forward.",
        aliases=["skip"],
        action_path="adventure.commands.move.move",
    )
    yield cmd


@pytest.fixture
def slide_cmd():
    cmd = Command(
        name="slide",
        desc="running and coming to a stop on your knees",
        help_text="for stealing home base",
        aliases=[],
        action_path="adventure.commands.move.move",
    )
    yield cmd


class TestCommand:
    """Test for command function."""

    def test_command_init(self, hop_cmd):
        """Test the command initializer."""
        assert isinstance(hop_cmd, Command)
        assert hop_cmd.name == "hop"
        assert str(hop_cmd) == "hop - A sudden motion forward"

    def test_command_init_fail(self):
        """Test a bad action path for a command init."""
        with pytest.raises(CommandNotFoundError):
            Command(
                name="slide",
                desc="running and coming to a stop on your knees",
                help_text="for stealing home base",
                aliases=[],
                action_path="adventure.commands.move.slide",
            )

    def test_command_init_bad_import_action(self):
        """Test an action path that cannot be resolved."""
        with pytest.raises(ImportError):
            Command(
                name="slide",
                desc="running and coming to a stop on your knees",
                help_text="for stealing home base",
                aliases=[],
                action_path="adventure.commands.slide.slide",
            )

    def test_command_init_no_action_path(self):
        with pytest.raises(ValueError):
            Command(
                name="rock",
                desc="flailing around to your favorite music",
                help_text="purely for show",
                aliases=[],
                action_path="",
            )

    def test_command_compare(self, hop_cmd, slide_cmd):
        """Test if commands can be compared."""
        other_cmd = hop_cmd
        assert other_cmd == hop_cmd
        assert hop_cmd != slide_cmd
        with pytest.raises(ValueError):
            assert hop_cmd == "NotAnAction"
