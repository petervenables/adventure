"""Main runner of the adventure game."""

import sys
from adventure.utils import escape_hatch
from adventure.exceptions import CommandNotFoundError
from adventure.game import Game
from adventure.ui.prompt import Prompt
from adventure.ui.consoleui import ConsoleUI

ui = ConsoleUI()
prompt: Prompt = Prompt(ui=ui)
prompt.load()


@escape_hatch(
    start_message=prompt.prepare("greeting", "yellow"),
    end_message=prompt.prepare("farewell", "blue"),
)
def main():
    """The main thing."""
    game: Game = Game(map_file="adventure/data/maps/start_map.yml")

    prompt.show("opening", "blue")

    while game.is_running:
        stmt = prompt.read_input()
        try:
            action = game.interpreter.prepare(stmt)
            result = action.verb.do_action(game, action.args)
            if result:
                prompt.display(result, "green")
        except CommandNotFoundError:
            prompt.show("unknown_action", "red")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
