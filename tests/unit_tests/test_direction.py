"""Unit tests for Direction enum and related functionality."""

import pytest

from adventure.map.direction import Direction, normalize_direction


def test_aliases_and_from_string():
    """canonical and alias lookup"""
    assert Direction.from_string("north") is Direction.NORTH
    assert Direction.from_string("N") is Direction.NORTH
    assert Direction.from_string("n") is Direction.NORTH
    assert Direction.from_string("Ne") is Direction.NORTHEAST


def test_numeric_value_and_int_conversion():
    """Ensure canonical values are integers and int() works"""
    assert isinstance(int(Direction.NORTH), int)
    assert int(Direction.NORTH) == 0
    assert Direction.NORTH == 0

    # Different direction has different value
    assert int(Direction.EAST) != int(Direction.SOUTH)
    assert Direction.EAST == int(Direction.EAST)


def test_aliases_for_unknown():
    """Unknown direction returns lowercase of input as fallback"""
    assert Direction.aliases_for("not-a-dir") == ["not-a-dir"]


def test_aliases_for_class():
    """Aliases for Direction class"""
    assert Direction.aliases_for(Direction.SOUTH) == ["south", "s"]
    assert Direction.aliases_for(Direction.UP) == ["up", "ceiling"]
    assert not Direction.aliases_for(None)
    assert Direction.aliases_for("south") == ["south", "s"]


def test_from_string_none_and_unknown():
    """None and unknown strings return None"""
    assert Direction.from_string(None) is None
    assert Direction.from_string("") is None
    assert Direction.from_string("nope") is None


def test_normalize_direction():
    """normalize_direction returns canonical name or None"""
    assert normalize_direction("n") == "NORTH"
    assert normalize_direction("NORTH") == "NORTH"
    assert normalize_direction("southwest") == "SOUTHWEST"
    assert normalize_direction("Ceiling") == "UP"
    assert normalize_direction("not-a-dir") is None
    assert normalize_direction("") is None
    assert normalize_direction(None) is None
