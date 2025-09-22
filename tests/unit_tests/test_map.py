"""Unit tests for the Map class."""

import pytest

from adventure.map.map import Map
from adventure.exceptions import BadYamlError

TEST_DATA_DIR = "tests/data"


class TestMap:
    """Test the Map class."""

    def test_load_map(self):
        """Test loading a map from a YAML file."""
        game_map = Map(base_data_dir=TEST_DATA_DIR, file_name="test_map.yml")
        assert isinstance(game_map, Map)
        assert game_map.name == "Test Map"
        assert game_map.description == "Test Map Description"
        assert str(game_map) == "Test Map - Test Map Description"
        assert game_map.base_data_dir == TEST_DATA_DIR
        assert len(game_map.rooms) == 3
        assert game_map.start_room == 1
        assert game_map.get_room(1).name == "Room One"
        assert game_map.get_room(2).name == "Room Two"
        assert game_map.get_room(3).name == "Room Three"
        with pytest.raises(IndexError):
            game_map.get_room(4)

    def test_load_map_default_base_dir(self):
        """Test loading a map with default base data directory."""
        # Setting the base_data_dir to DEFAULT_DATA_DIR means the room files will not be found
        with pytest.raises(NotADirectoryError):
            Map(base_data_dir="notfound", file_name="test_map.yml")

    def test_load_map_invalid_map(self):
        """Test loading a map from an invalid YAML file."""
        with pytest.raises(FileNotFoundError):
            Map(file_name="non_existent_map.yml", base_data_dir=TEST_DATA_DIR)
        with pytest.raises(ValueError):
            Map(file_name="", base_data_dir=TEST_DATA_DIR)
        with pytest.raises(NotADirectoryError):
            Map(file_name="dtest_map.yml", base_data_dir="non_existent_dir")

    def test_load_map_bad_yaml(self):
        """Test loading a map from a badly formatted YAML file."""
        # Create a temporary bad YAML file for testing
        with open(f"{TEST_DATA_DIR}/bad_map.yml", "w", encoding="utf-8") as f:
            f.write("This is not valid YAML")
        with pytest.raises(BadYamlError):
            Map(file_name="bad_map.yml", base_data_dir=TEST_DATA_DIR)

    def test_load_map_duplicate_room_ids(self):
        """Test loading a map with duplicate room IDs."""
        with pytest.raises(ValueError):
            Map(file_name="test_map_duplicate.yml", base_data_dir=TEST_DATA_DIR)

    def test_load_map_missing_room_id(self):
        """Test loading a map with a room missing an ID."""
        with pytest.raises(ValueError):
            Map(file_name="test_map_unset_room_id.yml", base_data_dir=TEST_DATA_DIR)
