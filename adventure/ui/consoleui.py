"""ConsoleUI class for displaying messages and getting input in a console environment.

This class inherits from BaseUI and implements methods for console interaction.
"""
import textwrap
from colorama import init, Fore, Style
from adventure.ui.baseui import BaseUI
from adventure.defaults import DEFAULT_CONSOLE_WIDTH

class ConsoleUI(BaseUI):
    """Console user interface for the adventure game."""

    def __init__(self):
        """Initialize the console UI."""
        # Colorama
        init()
        self.width = DEFAULT_CONSOLE_WIDTH
        self.wrapper = textwrap.TextWrapper(width=self.width)


    def display_message(self, message: str, color: str = None):
        """Display a message in the console."""
        if color:
            print(self.wrapper.fill(self.show_color(message, color)))
        else:
            print(self.wrapper.fill(message))

    def get_input(self, prompt: str = "") -> str:
        """Get input from the user in the console."""
        return input(prompt)

    def show_color(self, msg: str, color: str) -> str:
        """return a message from the prompts using the color text."""
        if not msg:
            raise ValueError("Message cannot be empty.")
        if color in ["red", "yellow", "green", "blue", "magenta"]:
            color_func = getattr(Fore, color.upper(), None)
            return color_func + msg + Style.RESET_ALL
        else:
            return msg
