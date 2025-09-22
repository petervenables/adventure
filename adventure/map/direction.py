"""Direction enum with aliases.

This module provides an IntEnum `Direction` where each member has an integer
value, and helper functions to map aliases / strings to canonical directions.
"""

from enum import IntEnum
from typing import List, Optional, Union


# canonical -> aliases (canonical first)
_ALIASES: dict[str, List[str]] = {
    "north": ["north", "n"],
    "northeast": ["northeast", "ne"],
    "east": ["east", "e"],
    "southeast": ["southeast", "se"],
    "south": ["south", "s"],
    "southwest": ["southwest", "sw"],
    "west": ["west", "w"],
    "northwest": ["northwest", "nw"],
    "up": ["up", "ceiling"],
    "down": ["down", "floor"],
}


# reverse lookup: alias -> canonical (lowercase)
_ALIAS_TO_CANONICAL: dict[str, str] = {}
for _canon, aliases in _ALIASES.items():
    for a in aliases:
        _ALIAS_TO_CANONICAL[a.lower()] = _canon


class Direction(IntEnum):
    """Set the direction the player wants to move in."""

    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    UP = 8
    DOWN = 9

    @classmethod
    def from_string(cls, s: Optional[str]) -> Optional["Direction"]:
        """Return the Direction for a canonical name or alias, or None.

        Examples:
            Direction.from_string('n') -> Direction.NORTH
            Direction.from_string('north') -> Direction.NORTH
        """
        if not s:
            return None
        key = s.strip().lower()
        canonical = _ALIAS_TO_CANONICAL.get(key)
        if not canonical:
            return None
        return cls[canonical.upper()]

    @classmethod
    def aliases_for(cls, arg: Union[str, "Direction"]) -> List[str]:
        """Return the list of aliases (canonical first) for a Direction or string.

        If `arg` is a Direction instance, returns the aliases for that canonical.
        If `arg` is a string, resolves it to a canonical (via alias lookup) and
        returns the aliases; if unknown, returns [arg.lower()].
        """
        if isinstance(arg, cls):
            canonical = arg.name.lower()
            return list(_ALIASES.get(canonical, [canonical]))
        if not arg:
            return []
        key = arg.strip().lower()
        canonical = _ALIAS_TO_CANONICAL.get(key)
        if canonical:
            return list(_ALIASES[canonical])
        return [key]


def normalize_direction(value: str) -> Optional[str]:
    """Return the canonical member name (e.g. 'NORTH') for a given string or None."""
    inst = Direction.from_string(value)
    if inst is None:
        return None
    return inst.name
