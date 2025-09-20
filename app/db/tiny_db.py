from functools import lru_cache
from pathlib import Path

from tinydb import TinyDB


@lru_cache
def get_db(db_path: str = "db.json") -> TinyDB:
    """Get TinyDB instance with caching to ensure singleton behavior."""
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(db_path)
