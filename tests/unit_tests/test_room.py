"""Tests for the Room class."""

import pytest

from adventure.exceptions import ItemNotFoundError
from adventure.rooms.room import Room
from adventure.rooms.wall import Wall
from adventure.rooms.door import Door
from adventure.map.direction import Direction
from adventure.items.item import Item


class TestRoom:
    def test_room_creation_and_defaults(self):
        room = Room(name="Test Room", short_desc="short", long_desc="long")
        assert room.name == "Test Room"
        assert room.short_desc == "short"
        assert room.long_desc == "long"
        # visited flag should default to False
        assert hasattr(room, "visited")
        assert room.visited is False

    def test_add_wall_and_doors(self):
        room = Room(name="Door Room", short_desc="short", long_desc="long")
        north_wall = Wall(
            name="north wall",
            short_desc="north short",
            long_desc="north long",
            location=Direction.NORTH,
            doors=[],
        )
        room.add_wall(wall=north_wall, location=Direction.NORTH)
        assert len(room.get_walls()) == 1
        # no doors yet
        assert room.show_doors() == ""

        d = Door(name="Steel Door", short_desc="a steel door", long_desc="heavy")
        north_wall.add_door(door=d)
        # show_doors should include the direction
        assert "[ NORTH ]" in room.show_doors()
        exits = room.get_exits()
        assert len(exits) == 1
        doors = room.get_doors()
        assert len(doors) == 1
        assert doors[0].name == "Steel Door"

    def test_in_room_item_and_wall_lookup(self):
        room = Room(name="Find Room", short_desc="short", long_desc="long")
        rock = Item(
            name="Rock", short_desc="a small rock", long_desc="a fist-sized rock"
        )
        room.contents.append(rock)
        found = room.in_room("rock")
        assert isinstance(found, list)
        assert found[0]["what"].name == "Rock"

        # add a wall and door and find them by name/location
        south_wall = Wall(
            name="south wall",
            short_desc="south short",
            long_desc="south long",
            location=Direction.SOUTH,
            doors=[],
        )
        room.add_wall(wall=south_wall, location=Direction.SOUTH)
        door = Door(
            name="Wooden Door", short_desc="a wooden door", long_desc="old wood"
        )
        south_wall.add_door(door=door)
        found_wall = room.in_room("south")
        # should find the wall/door entry by wall name
        assert any(item["where"].lower() == "south" for item in found_wall)

    def test_connect_exits_sets_door_leads_to(self):
        room = Room(name="Connect Room", short_desc="short", long_desc="long")
        east_wall = Wall(
            name="east wall",
            short_desc="east short",
            long_desc="east long",
            location=Direction.EAST,
            doors=[],
        )
        room.add_wall(wall=east_wall, location=Direction.EAST)
        door = Door(name="Portal", short_desc="a portal", long_desc="shimmering")
        east_wall.add_door(door=door)
        # connect exits using a mapping of direction -> room id
        room.connect_exits({"east": 42})
        assert east_wall.doors[0].leads_to == 42

    def test_add_door_to_room(self):
        room = Room(name="Add Door Room", short_desc="short", long_desc="long")
        west_wall = Wall(
            name="west wall",
            short_desc="west short",
            long_desc="west long",
            location=Direction.WEST,
            doors=[],
        )
        room.add_wall(wall=west_wall, location=Direction.WEST)
        door = Door(name="Iron Gate", short_desc="an iron gate", long_desc="rusty iron")
        room.add_door(door=door, location=Direction.WEST)
        assert west_wall.has_door()
        assert west_wall.get_door().name == "Iron Gate"

    def test_in_room_item_not_found(self):
        room = Room(name="Empty Room", short_desc="short", long_desc="long")
        with pytest.raises(ItemNotFoundError):
            room.in_room("nonexistent")

    def test_in_room_item_found(self):
        room = Room(name="Item Room", short_desc="short", long_desc="long")
        item = Item(name="Key", short_desc="a small key", long_desc="a tiny brass key")
        room.contents.append(item)
        result = room.in_room("key")
        assert len(result) == 1
        assert result[0]["what"].name == "Key"

    def test_in_room_named_door(self):
        room = Room(name="Door Room", short_desc="short", long_desc="long")
        wall = Wall(
            name="north wall",
            short_desc="north short",
            long_desc="north long",
            location=Direction.NORTH,
            doors=[],
        )
        room.add_wall(wall=wall, location=Direction.NORTH)
        door = Door(name="Front Door", short_desc="a front door", long_desc="wooden")
        wall.add_door(door=door)
        result = room.in_room("Front Door")
        assert len(result) == 1
        assert result[0]["what"].name == "Front Door"

    def test_in_room_wall_no_door(self):
        room = Room(name="Wall Room", short_desc="short", long_desc="long")
        wall = Wall(
            name="east wall",
            short_desc="east short",
            long_desc="east long",
            location=Direction.EAST,
            doors=[],
        )
        room.add_wall(wall=wall, location=Direction.EAST)
        result = room.in_room("east")
        assert len(result) == 1
        assert result[0]["what"].name == "east wall"
