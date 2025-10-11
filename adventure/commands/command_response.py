"""Command response module."""

from typing import Optional


class ResponseMessage:
    """A class to encapsulate a message and its color."""

    message: str
    color: str

    def __init__(self, message: str, color: str) -> None:
        self.message = message
        self.color = color

    def __str__(self) -> str:
        return self.message


class CommandResponse:
    """A class to encapsulate the response from a command action."""

    messages: list[ResponseMessage]

    def __init__(
        self, message: Optional[str] = None, color: Optional[str] = "blue"
    ) -> None:
        self.messages = []
        if message:
            self.add_message(message, color)

    def add_message(self, message: str, color: str) -> None:
        """Add a message to the response.

        Args:
            message (str): The message text.
            color (str): The color to display the message in.

        Returns:
            None

        """
        self.messages.append(ResponseMessage(message, color))

    def __str__(self) -> str:
        return "\n".join(str(msg) for msg in self.messages)
