"""Main runner of the adventure game."""

import sys
from adventure.game import Game
from adventure.defaults import DEFAULT_DATA_DIR, DEFAULT_MAP_FILE, DEFAULT_COMMANDS_FILE


def main():
    """The main thing."""
    game: Game = Game(
        base_data_dir=DEFAULT_DATA_DIR,
        map_file_name=DEFAULT_MAP_FILE,
        cmd_file_name=DEFAULT_COMMANDS_FILE,
    )
    try:
        game.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
