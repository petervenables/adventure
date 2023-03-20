"""adventure/utils -- special things to do neat stuff.

This is not my code. I got it from Adrian Causby.
https://towardsdatascience.com/how-to-add-an-escape-hatch-to-your-python-run-in-two-steps-7d6818f58f14

"""
# Base Library Packages
import _thread

# Third Party Packages
from functools import wraps
from pynput import keyboard

from colorama import Fore, Style

def escape_hatch(
    start_message="",
    end_message="",
    keyboard_key=keyboard.Key.esc,
    # key_string="Esc",
):
    """Function to decorate API calls as an escape hatch
    Args:
      start_message (str): start message to show decorator started
      end_message (str): end message to show decorator end
      method: method to be decorated - the inner function
      keyboard_key (keyboard.Key or keyboard.KeyCode):
    interrupt key to listen for, in our case is the escape key
      key_string (str): string representation of key to print in message"""

    def decorate(func):
        def keyboard_handler(key, escape_key=keyboard_key):
            if key == escape_key:
                print(Fore.LIGHTRED_EX + "    Program terminated by user" + Style.RESET_ALL)
                _thread.interrupt_main()

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Handle keyboard interrupts by user
            with keyboard.Listener(on_press=keyboard_handler):
                print(Fore.LIGHTGREEN_EX + start_message + Style.RESET_ALL)
                # print(
                #    f"    Press '{key_string}' any time to terminate the program",
                # )
                # Do inner function
                result = func(*args, **kwargs)

                # Print message after API response received
                print(Fore.LIGHTRED_EX + end_message + Style.RESET_ALL)
            return result

        return wrapper

    return decorate
