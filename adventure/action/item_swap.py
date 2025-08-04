"""item_swap -- for swapping an item from one inventory container to another."""

from adventure.inventory import Inventory
from adventure.constants import location_mod_words
from adventure.items.item import Item


def item_swap(args: list, inv: Inventory) -> str:
    """Let player move item from one container to another."""
    dest: str = None
    mover: str = None
    source = None
    for arg in args:
        if arg in inv.list_all_containers():
            dest = arg
        elif arg in location_mod_words:
            continue
        else:
            found: list[dict[str, Item]] = inv.find_item(arg)
            if len(found) > 0:
                mover = found[0]["what"].name
                source = found[0]["where"]
    if len(dest) > 0 and mover is not None and source is not None:
        if inv.swap_container_item(source=source, dest=dest, item_name=mover):
            return f"You relocate the {mover} from {source} to {dest}."
    return "You can't swap those things."
