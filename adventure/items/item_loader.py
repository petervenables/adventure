import yaml
from adventure.items.item import Item, HandheldItem, ThrowableItem

CLASS_MAP = {
    "handheld": HandheldItem,
    "throwable": ThrowableItem,
}


def load_item_from_yaml(file_path: str) -> Item:
    """Load an item from a YAML file."""
    with open(file_path, "r", encoding="utf8") as file:
        data = yaml.safe_load(file)

    base_classes = [Item]
    for cls_name in data.get("classes", []):
        if cls_name not in CLASS_MAP:
            raise ValueError(f"Unknown item class: {cls_name}")
        cls = CLASS_MAP[cls_name]
        if cls:
            for i, base in enumerate(base_classes):
                if issubclass(cls, base):
                    base_classes[i] = cls
                    break
            else:
                base_classes.append(cls)
    composite_item = type(data["name"].capitalize() + "Item", tuple(base_classes), {})
    args = {key: value for key, value in data.items() if key != "classes"}
    return composite_item(**args)
