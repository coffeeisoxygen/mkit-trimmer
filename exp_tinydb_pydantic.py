"""testing purposes and experimenting."""

from pydantic import BaseModel
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


class Item(BaseModel):
    name: str
    value: float


class ItemInDB(Item):
    id: int


db = TinyDB(storage=MemoryStorage)
table = db.table("items")


def doc_to_model(doc, model_cls):
    if doc:
        doc_dict = doc.copy()
        doc_dict["id"] = doc.doc_id
        return model_cls(**doc_dict)
    return None


def add_item(item: Item) -> ItemInDB:
    data = item.model_dump(mode="json")
    doc_id = table.insert(data)
    data["id"] = doc_id
    return ItemInDB(**data)


def get_item_by_id(item_id: int) -> ItemInDB | None:
    item_doc = table.get(doc_id=item_id)
    return doc_to_model(item_doc, ItemInDB)


def update_item(item_id: int, item: Item) -> ItemInDB | None:
    if table.contains(doc_id=item_id):
        data = item.model_dump(mode="json")
        table.update(data, doc_ids=[item_id])
        updated_doc = table.get(doc_id=item_id)
        return doc_to_model(updated_doc, ItemInDB)
    return None


def delete_item(item_id: int) -> bool:
    if table.contains(doc_id=item_id):
        table.remove(doc_ids=[item_id])
        return True
    return False


def list_items() -> list[ItemInDB]:
    """List all items in the database.

    Returns:
    -------
    list[ItemInDB]
        List of all items stored in the database.
    """
    return [
        item
        for item in (doc_to_model(doc, ItemInDB) for doc in table.all())
        if item is not None
    ]


def main():
    # Create
    item1 = Item(name="Item1", value=10.5)
    item2 = Item(name="Item2", value=20.0)
    added_item1 = add_item(item1)
    added_item2 = add_item(item2)
    print(f"Added Item 1: {added_item1}")
    print(f"Added Item 2: {added_item2}")

    # Read
    fetched_item = get_item_by_id(added_item1.id)
    print(f"Fetched Item by ID: {fetched_item}")

    # Update
    updated_item = update_item(added_item1.id, Item(name="UpdatedItem1", value=99.9))
    print(f"Updated Item: {updated_item}")

    # Delete
    delete_result = delete_item(added_item2.id)
    print(f"Deleted Item 2: {delete_result}")

    # List
    print("All items in the database:")
    for item in list_items():
        print(item)


if __name__ == "__main__":
    main()
