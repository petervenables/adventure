"""Base UI class for the adventure game.
This class defines the interface for user interaction in the game.
It should be implemented by any UI class that wants to provide a user interface.
"""

from abc import ABC, abstractmethod


class BaseUI(ABC):
    """Abstract base class for user interface in the adventure game."""

    @abstractmethod
    def display_message(self, message: str, color: str = None):
        """Display a message to the user."""

    @abstractmethod
    def get_input(self, prompt: str = "") -> str:
        """Get input from the user."""

    @abstractmethod
    def show_color(self, msg: str, color: str) -> str:
        """Return a message from the prompts using the specified color."""
        raise NotImplementedError("This method should be implemented by subclasses.")
