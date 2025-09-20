from functools import lru_cache
from pathlib import Path

from tinydb import TinyDB


@lru_cache
def get_db(db_path: str | None = "db.json") -> TinyDB:
    """Get TinyDB instance with caching to ensure singleton behavior."""
    db_file = Path(db_path := "db.json" if db_path is None else db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Kembali ke TinyDB default tanpa BetterJSONStorage
    return TinyDB(db_path)
