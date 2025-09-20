"""Base database manager using TinyDB."""

from pathlib import Path
from typing import Any

from loguru import logger
from tinydb import Query, TinyDB


class BaseDBManager:
    """Base class for TinyDB managers with table support."""

    def __init__(self, db_path: str, table_name: str):
        """Initialize database manager for a specific table."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(self.db_path)
        self.table = self.db.table(table_name)
        self.query = Query()

    def __del__(self):
        """Close database connection."""
        if hasattr(self, "db"):
            self.db.close()

    def insert(self, data: dict[str, Any]) -> int:
        """Insert a new record into the table."""
        try:
            doc_id = self.table.insert(data)
        except Exception as e:
            logger.error(f"Failed to insert record: {e}")
            raise
        else:
            logger.info(f"Inserted record with ID: {doc_id}")
            return doc_id

    def get_all(self) -> list[dict[str, Any]]:
        """Get all records from the table."""
        return [dict(doc) for doc in self.table.all()]

    def get_by_id(self, doc_id: int) -> dict[str, Any] | None:
        """Get record by ID from the table."""
        doc = self.table.get(doc_id=doc_id)
        # Ensure only a dict or None is returned, never a list
        if doc is None:
            return None
        if isinstance(doc, dict):
            return dict(doc)
        # If somehow a list is returned, return None (should not happen)
        return None

    def update(self, doc_id: int, data: dict[str, Any]) -> bool:
        """Update record by ID in the table."""
        try:
            result = self.table.update(data, doc_ids=[doc_id])
            success = len(result) > 0
        except Exception as e:
            logger.error(f"Failed to update record {doc_id}: {e}")
            raise
        else:
            if success:
                logger.info(f"Updated record ID: {doc_id}")
            return success

    def delete(self, doc_id: int) -> bool:
        """Delete record by ID from the table."""
        try:
            result = self.table.remove(doc_ids=[doc_id])
            success = len(result) > 0
        except Exception as e:
            logger.error(f"Failed to delete record {doc_id}: {e}")
            raise
        else:
            if success:
                logger.info(f"Deleted record ID: {doc_id}")
            return success

    def search(self, condition: Any) -> list[dict[str, Any]]:
        """Search records with condition in the table."""
        return list(self.table.search(condition))

    def count(self) -> int:
        """Count total records in the table."""
        return len(self.table)

    def truncate(self) -> None:
        """Remove all records from the table."""
        self.table.truncate()
        logger.info("Truncated all records in table")
