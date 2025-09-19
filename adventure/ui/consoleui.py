"""ConsoleUI class for displaying messages and getting input in a console environment.

This class inherits from BaseUI and implements methods for console interaction.
"""

import textwrap
import readchar
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
        """Read text-based commands from the user, handling special keys."""
        print("> ", end="", flush=True)
        chars = []
        while True:
            ch = readchar.readkey()
            if ch == readchar.key.ESC:
                # User wants out.
                raise SystemExit
            if ch == readchar.key.BACKSPACE:
                # back up and remove from read chars
                chars.pop()
                # Move cursor back, overwrite with space, move back again
                print('\b \b', end='', flush=True)
            elif ch == '\r' or ch == '\n':
                print()  # Move to next line
                return ''.join(chars).rstrip()
            else:
                print(ch, end="", flush=True)
                chars.append(ch)

    def show_color(self, msg: str, color: str) -> str:
        """return a message from the prompts using the color text."""
        if not msg:
            raise ValueError("Message cannot be empty.")
        if color in ["red", "yellow", "green", "blue", "magenta"]:
            color_func = getattr(Fore, color.upper(), None)
            return color_func + msg + Style.RESET_ALL
        else:
            return msg
