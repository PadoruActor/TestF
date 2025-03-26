"""
Database configuration for Tron Address Info API.

Sets up SQLAlchemy engine, session factory, and base model.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database engine with connection pooling
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False  # Set to True for debug logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session.

    Yields:
        Database session

    Ensures:
        Session is properly closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()