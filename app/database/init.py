"""Database initialization and migration script."""

from loguru import logger

from app.config import get_all_settings
from app.database.digipos import DigiposDBManager
from app.database.member import MemberDBManager


def init_databases() -> tuple[MemberDBManager, DigiposDBManager]:
    """Initialize databases with data from config (single db file, multiple tables)."""
    settings = get_all_settings()
    db_path = getattr(settings.application, "db_path", "data/appdb.json")
    member_db = MemberDBManager(db_path, table_name="members")
    digipos_db = DigiposDBManager(db_path, table_name="digipos")
    return member_db, digipos_db


def migrate_from_config() -> None:
    """Migrate existing data from config.toml to databases."""
    logger.info("Starting database migration from config...")

    member_db, digipos_db = init_databases()

    # Sample data migration (since we removed from config.toml)
    sample_members = [
        {
            "name": "member",
            "ipaddress": "10.0.0.1",
            "report_url": "http://10.0.0.1/report",
            "is_allowed": True,
            "rate_limiter": "1/minute",
        },
        {
            "name": "member",
            "ipaddress": "127.0.0.1",
            "report_url": "http://127.0.0.1/report",
            "is_allowed": True,
            "rate_limiter": "1/minute",
        },
    ]

    sample_digipos = [
        {
            "username": "user1",
            "password": "pass1",
            "pin": "1234",
            "base_url": "http://10.0.0.3:10003/",
            "time_out": 30,
            "retries": 3,
        },
        {
            "username": "user2",
            "password": "pass2",
            "pin": "5678",
            "base_url": "http://10.0.0.4:10004/",
            "time_out": 25,
            "retries": 2,
        },
    ]

    # Migrate members (only if database is empty)
    if member_db.count() == 0:
        for member in sample_members:
            try:
                member_db.create_member(**member)
            except ValueError as e:
                logger.warning(f"Skipped member migration: {e}")

    # Migrate digipos accounts (only if database is empty)
    if digipos_db.count() == 0:
        for account in sample_digipos:
            try:
                digipos_db.create_account(**account)
            except ValueError as e:
                logger.warning(f"Skipped digipos migration: {e}")

    logger.info("Database migration completed!")


if __name__ == "__main__":
    migrate_from_config()
