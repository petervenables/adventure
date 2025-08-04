"""adventure/game -- track the game state and history."""

from adventure.rooms.room import Room
from adventure.interpreter import Interpreter
from adventure.map.map import Map
from adventure.player.player import Player


class Game:
    """This is the game class."""

    is_running: bool
    current_loc: Room = None
    interpreter: Interpreter
    map: Map = Map()
    player: Player = Player()

    def __init__(self, map_file: str):
        self.is_running = True
        self.interpreter = Interpreter()
        self.map.load_yaml(map_file)
        self.current_loc = self.map.get_room(0)
