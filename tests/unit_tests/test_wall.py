"""Test Adventure Room Wall functionality."""

import pytest
from adventure.rooms.wall import Wall
from adventure.rooms.door import Door
from adventure.map.direction import Direction


class TestWall:
    """Test Wall class."""

    @pytest.fixture(autouse=True)
    def good_wall(self):
        """Fixture for a good wall."""
        wall = Wall(
            name="north wall",
            short_desc="short",
            long_desc="long desc",
            location=Direction.NORTH,
            doors=[],
        )
        return wall

    def test_wall_creation(self):
        """Test creating a wall."""
        direction = Direction.NORTH
        wall = Wall(
            name="north wall",
            short_desc="short",
            long_desc="long desc",
            location=direction,
            doors=[],
        )
        assert wall.location == Direction.NORTH
        assert wall.name == "north wall"
        assert not wall.doors
        assert not wall.has_door()

    def test_add_door(self, good_wall):
        """Test adding a door to the wall."""
        wall: Wall = good_wall
        assert isinstance(good_wall, Wall)
        assert not wall.has_door()
        a_door = Door(name="Door1", short_desc="A door", long_desc="A wooden door")
        wall.add_door(door=a_door)
        assert len(wall.doors) == 1
        assert wall.has_door()
        assert wall.doors[0].name == "Door1"

    def test_get_door(self, good_wall):
        """Test getting the first door from the wall."""
        wall: Wall = good_wall
        a_door = Door(name="Door1", short_desc="A door", long_desc="A wooden door")
        assert wall.get_door() is None
        wall.add_door(door=a_door)
        assert wall.get_door().name == "Door1"
