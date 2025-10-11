"""adventure/rooms/events -- room event classes separated to avoid circular imports.

This module contains event-related classes for rooms. Moving RoomEvent here
decouples the runtime import graph between `room` and `room_event`.
"""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from adventure.rooms.room import Room


class RoomEvent:
    """Define an event that can occur in a room."""

    def __init__(
        self,
        trigger_condition: Callable[["Room"], bool],
        action: Callable[["Room"], None],
    ):
        self.trigger_condition = trigger_condition  # A callable that returns True/False
        self.action = action  # A callable that performs the event action
        self.fired = False

    def is_triggered(self, room: "Room") -> bool:
        """Check if the event's trigger condition is met."""
        return self.trigger_condition(room) and not self.fired

    def fire(self, room: "Room"):
        """Fire the event action."""
        if not self.fired:
            self.action(room)
            self.fired = True
