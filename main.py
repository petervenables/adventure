"""Main runner of the adventure game."""

import sys
from adventure.game import Game

def main():
    """The main thing."""
    game: Game = Game(map_file="adventure/data/maps/start_map.yml")
    try:
        game.run()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
