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

    base_data_dir: str = ""
    is_running: bool
    current_loc: Room = None
    ui: BaseUI
    prompt: Prompt
    interpreter: Interpreter
    map: Map
    player: Player = Player()

    def __init__(self, base_data_dir: str, map_file_name: str, cmd_file_name: str):
        if not base_data_dir:
            raise ValueError("A base data directory must be provided.")
        if not map_file_name:
            raise ValueError("A map file name must be provided.")
        if not cmd_file_name:
            raise ValueError("A commands file name must be provided.")
        self.base_data_dir = base_data_dir
        self.is_running = True
        self.interpreter = Interpreter(commands_file=f"{base_data_dir}/{cmd_file_name}")
        self.ui = ConsoleUI()
        self.prompt = Prompt(ui=self.ui)
        self.map = Map(base_data_dir=base_data_dir, file_name=map_file_name)
        self.current_loc = self.map.get_room(self.map.start_room)
        self.prompt.load()

    def run(self):
        """Run the main game loop."""
        self.prompt.show("greeting", "yellow")
        self.prompt.show("opening", "blue")
        while self.is_running:
            try:
                stmt = self.prompt.read_input()
                if not stmt:
                    continue
                action = self.interpreter.prepare(stmt)
                result = action.verb.do_action(self, action.args, action=action.tokens[0])
                if result:
                    self.prompt.display(result, "green")
            except BadStatementError:
                self.prompt.show("bad_statement", "red")
            except CommandNotFoundError:
                self.prompt.show("unknown_action", "red")
            except SystemExit:
                self.prompt.show("Escape key pressed: exiting...")
        self.prompt.show("farewell", "blue")
