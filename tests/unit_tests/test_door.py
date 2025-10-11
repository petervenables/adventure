"""Tests for the Door class."""

from adventure.rooms.door import Door


class TestDoor:
    def test_door_defaults(self):
        d = Door(name="TestDoor", short_desc="a test door", long_desc="long")
        assert d.name == "TestDoor"
        assert d.short_desc == "a test door"
        assert d.long_desc == "long"
        # default flags
        assert d.is_open is True
        assert d.is_locked is False
        assert d.is_blocked is False
        assert d.leads_to is None

    def test_lock_unlock_open_close_block_unblock(self):
        d = Door(name="D", short_desc="s", long_desc="l")
        d.lock()
        assert d.is_locked is True
        d.unlock()
        assert d.is_locked is False

        d.close()
        assert d.is_open is False
        d.open()
        assert d.is_open is True

        d.block()
        assert d.is_blocked is True
        d.unblock()
        assert d.is_blocked is False

    def test_connect_sets_leads_to(self):
        d = Door(name="Portal", short_desc="portal", long_desc="shimmery")
        d.connect(123)
        assert d.leads_to == 123
