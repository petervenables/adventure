"""Main runner of the adventure game."""

import sys
from colorama import init
from adventure.utils import escape_hatch
from adventure.exceptions import CommandNotFoundError
from adventure.game import Game
from adventure.prompt import Prompt

prompt: Prompt = Prompt()
prompt.load()


@escape_hatch(
    start_message=prompt.yellow("greeting"), end_message=prompt.blue("farewell")
)
def main():
    """The main thing."""
    game: Game = Game(map_file="adventure/data/maps/start_map.yml")

    print(prompt.blue("opening"))

    while game.is_running:
        stmt = prompt.read_input()
        try:
            action = game.interpreter.prepare(stmt)
            print(action.verb.do_action(game, action.args))
        except CommandNotFoundError:
            print(prompt.red("unknown_action"))


if __name__ == "__main__":
    # colorama init
    init()
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
