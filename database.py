import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# For SQLite we need this connect_args; for others it's ignored
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create database tables if they do not exist.

    Note: This project does not use a full migration tool.
    We apply a small, safe migration for new columns when using SQLite.
    """
    Base.metadata.create_all(bind=engine)

    # Lightweight migrations (SQLite only)
    # WARNING: This is a simplified approach. For production, use Alembic or similar.
    try:
        from sqlalchemy import inspect, text
        import logging
        logger = logging.getLogger(__name__)

        # Only attempt ALTER TABLE on SQLite databases
        if not DATABASE_URL.startswith("sqlite"):
            return

        insp = inspect(engine)
        if "users" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("users")}
            if "password_hash" not in cols:
                logger.info("Migrating users table: adding password_hash column")
                with engine.begin() as conn:
                    # SQLite-specific ALTER TABLE - using text() for DDL statement
                    # Note: column name is hardcoded (not user input) so no SQL injection risk
                    conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                logger.info("Migration completed successfully")
    except Exception as e:
        # Non-fatal: DB might be already migrated or migration not needed
        import logging
        logging.getLogger(__name__).warning(f"Database migration skipped or failed: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
