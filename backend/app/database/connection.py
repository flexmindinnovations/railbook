"""
Database connection and session management.
Handles SQLAlchemy setup and table creation.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development"
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for table operations
metadata = MetaData()


async def create_tables():
    """Create all database tables."""
    try:
        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """
    Async database session for future async operations.
    Currently using sync sessions but prepared for async upgrade.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
