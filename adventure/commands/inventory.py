"""Inventory Command."""


def inv(game, *args, **kwargs):
    """Display the things you have on hand."""
    print(game.player.inventory.list_all_contents())
