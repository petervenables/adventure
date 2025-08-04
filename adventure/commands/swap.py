"""Swap Item Command."""

from adventure.action.item_swap import item_swap
from adventure.exceptions import ItemNotFoundError


def swap(game, *args, **kwargs) -> str:
    """Swap an item from one container to another."""
    try:
        return item_swap(*args, game.player.inventory)
    except ItemNotFoundError:
        return "You can't seem to locate that to swap it."
