import pytest

from adventure.map.direction import Direction


def test_aliases_and_from_string():
    # canonical and alias lookup
    assert Direction.from_string("north") is Direction.NORTH
    assert Direction.from_string("N") is Direction.NORTH
    assert Direction.from_string("n") is Direction.NORTH
    assert Direction.from_string("Ne") is Direction.NORTHEAST


def test_numeric_value_and_int_conversion():
    # Ensure canonical values are integers and int() works
    assert isinstance(int(Direction.NORTH), int)
    assert int(Direction.NORTH) == 0
    assert Direction.NORTH == 0

    # Different direction has different value
    assert int(Direction.EAST) != int(Direction.SOUTH)
    assert Direction.EAST == int(Direction.EAST)


def test_aliases_for_unknown():
    # unknown direction returns lowercase of input as fallback
    assert Direction.aliases_for("not-a-dir") == ["not-a-dir"]


def test_from_string_none_and_unknown():
    assert Direction.from_string(None) is None
    assert Direction.from_string("") is None
    assert Direction.from_string("nope") is None
