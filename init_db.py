"""
Database initialization script for Tron Address Info API.

Creates all necessary database tables using SQLAlchemy models.
"""

from app.database import Base, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """
    Initialize the database by creating all tables.

    Uses SQLAlchemy's metadata.create_all() to generate tables
    based on defined models.
    """
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise


if __name__ == "__main__":
    init_db()