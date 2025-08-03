"""adventure/exceptions."""


class CommandError(Exception):
    """Base class for command-related exceptions."""


class CommandNotFoundError(CommandError):
    """Raised when a command is not found in the command list."""


class InventoryError(Exception):
    """Base class for inventory-related exceptions."""


class ContainerCannotFitError(InventoryError):
    """Raised when an item cannot fit in a container due to size constraints."""


class ContainerFullError(InventoryError):
    """Raised when a container is full and cannot accept more items."""


class ItemNotFoundError(InventoryError):
    """Raised when an item is not found in a container or room."""


class ContainerNotFoundError(InventoryError):
    """Raised when a specified container does not exist."""


class DuplicateContainerError(InventoryError):
    """Raised when trying to create a container that already exists."""


class BadStatementError(CommandError):
    """Raised when a statement is malformed or cannot be processed."""
