from pathlib import Path

from BetterJSONStorage import BetterJSONStorage
from tinydb import TinyDB


def get_db(db_path: str = "db.json") -> TinyDB:
    """Get a TinyDB instance with BetterJSONStorage as the storage backend.

    This function creates a TinyDB instance with a specified database path and
    uses BetterJSONStorage for improved JSON handling.

    Args:
        db_path (str, optional): The path to the database file. Defaults to "db.json".

    Returns:
        TinyDB: A TinyDB instance with BetterJSONStorage as the storage backend.
    """
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(db_file, access_mode="r+", storage=BetterJSONStorage)
