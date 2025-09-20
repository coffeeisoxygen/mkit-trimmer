"""Digipos database manager."""

from typing import Any

from loguru import logger

from app.database.base import BaseDBManager


class DigiposDBManager(BaseDBManager):
    """Database manager for digipos accounts."""

    def __init__(self, db_path: str, table_name: str = "digipos"):
        super().__init__(db_path, table_name)

    def get_account_by_username(self, username: str) -> dict[str, Any] | None:
        """Get digipos account by username."""
        result = self.search(self.query.username == username)
        return result[0] if result else None

    def create_account(
        self,
        username: str,
        password: str,
        pin: str,
        base_url: str,
        time_out: int = 30,
        retries: int = 3,
    ) -> int:
        """Create a new digipos account."""
        # Check if account already exists
        existing = self.get_account_by_username(username)
        if existing:
            raise ValueError(f"Account with username {username} already exists")

        account_data = {
            "username": username,
            "password": password,
            "pin": pin,
            "base_url": base_url,
            "time_out": time_out,
            "retries": retries,
        }

        doc_id = self.insert(account_data)
        logger.info(f"Created digipos account: {username}")
        return doc_id

    def update_credentials(
        self, username: str, password: str | None = None, pin: str | None = None
    ) -> bool:
        """Update account credentials."""
        account = self.get_account_by_username(username)
        if not account:
            return False

        update_data = {}
        if password:
            update_data["password"] = password
        if pin:
            update_data["pin"] = pin

        if not update_data:
            return False

        doc_id = account.get("_doc_id") if account and "_doc_id" in account else None
        if not doc_id:
            return False
        return self.update(doc_id, update_data)

    def get_available_accounts(self) -> list[dict[str, Any]]:
        """Get all available digipos accounts."""
        return self.get_all()
