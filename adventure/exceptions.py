"""adventure/exceptions."""


class CommandError(Exception):
    pass


class CommandNotFoundError(CommandError):
    pass


class InventoryError(Exception):
    pass


class ItemNotFoundError(InventoryError):
    pass


class ContainerNotFoundError(InventoryError):
    pass


class DuplicateContainerError(InventoryError):
    pass


class BadStatementError(CommandError):
    pass
