"""adventure/direction -- handling compass movement operations."""
from typing import List

class Direction:
    name: str
    aliases: List[str]

    def __init__(self, name: str, aliases: List[str]):
        self.name = name
        self.aliases = aliases

    def match(self, direction: str) -> bool:
        if direction == self.name or direction in self.aliases:
            return True
        return False
