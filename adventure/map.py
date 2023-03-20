"""adventure/map -- a class to handle the world in which the player roams."""

from typing import List
from adventure import Room


class Map:
    rooms: List[Room]