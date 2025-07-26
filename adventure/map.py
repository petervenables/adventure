"""adventure/map -- a class to handle the world in which the player roams."""

from adventure.rooms.room import Room


class Map:
    rooms: list[Room]
