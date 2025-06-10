"""
Database connection module for MongoDB.
"""
import os
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

# MongoDB client
mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
mongodb = mongodb_client[settings.MONGODB_DB_NAME]


async def get_mongodb() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Get MongoDB database connection.
    
    Yields:
        AsyncIOMotorDatabase: MongoDB database connection
    """
    try:
        yield mongodb
    finally:
        # Connection is managed by the client
        pass
