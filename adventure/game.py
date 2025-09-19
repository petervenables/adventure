"""adventure/game -- track the game state and history."""

from adventure.rooms.room import Room
from adventure.interpreter import Interpreter
from adventure.map.map import Map
from adventure.player.player import Player
from adventure.ui.prompt import Prompt
from adventure.ui.consoleui import BaseUI, ConsoleUI
from adventure.exceptions import CommandNotFoundError, BadStatementError

class Game:
    """This is the game class."""

    is_running: bool
    current_loc: Room = None
    ui: BaseUI
    prompt: Prompt
    interpreter: Interpreter
    map: Map = Map()
    player: Player = Player()

    def __init__(self, map_file: str):
        self.is_running = True
        self.interpreter = Interpreter()
        self.ui = ConsoleUI()
        self.prompt = Prompt(ui=self.ui)
        self.map.load_yaml(map_file)
        self.current_loc = self.map.get_room(0)
        self.prompt.load()

    def run(self):
        """ Run the main game loop."""
        self.prompt.show("greeting", "yellow")
        self.prompt.show("opening", "blue")
        while self.is_running:
            try:
                stmt = self.prompt.read_input()
                if not stmt:
                    continue
                action = self.interpreter.prepare(stmt)
                result = action.verb.do_action(self, action.args)
                if result:
                    self.prompt.display(result, "green")
            except BadStatementError:
                self.prompt.show("bad_statement", "red")
            except CommandNotFoundError:
                self.prompt.show("unknown_action", "red")
            except SystemExit:
                self.prompt.show("Escape key pressed: exiting...")
        self.prompt.show("farewell", "blue")
