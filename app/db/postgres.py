"""
Database connection module for PostgreSQL with async support.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

# Create SQLAlchemy async engine
try:
    # Convert postgresql:// to postgresql+asyncpg:// if needed
    db_uri = str(settings.SQLALCHEMY_DATABASE_URI)
    if db_uri.startswith("postgresql://"):
        db_uri = db_uri.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    async_engine = create_async_engine(
        db_uri,
        pool_pre_ping=True,
        echo=settings.DB_ECHO_LOG
    )
    
    # Create async session factory
    # Create async session factory
    async_session_factory = async_sessionmaker(
        bind=async_engine, 
        expire_on_commit=False,
        class_=AsyncSession
    )
except Exception as e:
    print(f"Error creating async database engine: {e}")
    async_engine = None
    async_session_factory = None


async def create_db_and_tables():
    """
    Create database tables asynchronously.
    """
    if async_engine is not None:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    else:
        print("Warning: Database engine not available, skipping table creation")


async def get_async_session():
    """
    Get async database session.
    
    Yields:
        AsyncSession: Async database session
    """
    if async_session_factory is None:
        raise RuntimeError("Database engine not initialized")
        
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
