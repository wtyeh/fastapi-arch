"""
Log entry service module.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.repositories.log_entry import LogEntryRepository
from app.models.document import LogEntry


class LogEntryService:
    """
    Log entry service.
    """
    def __init__(self, repository: LogEntryRepository):
        """
        Initialize service.
        
        Args:
            repository (LogEntryRepository): Log entry repository
        """
        self.repository = repository
    
    async def get(self, db: AsyncIOMotorDatabase, log_id: str) -> Optional[LogEntry]:
        """
        Get log entry by ID.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            log_id (str): Log entry ID
            
        Returns:
            Optional[LogEntry]: Log entry instance or None
        """
        return await self.repository.get(db, log_id)
    
    async def get_all(self, db: AsyncIOMotorDatabase, *, skip: int = 0, limit: int = 100) -> List[LogEntry]:
        """
        Get all log entries.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            skip (int): Records to skip
            limit (int): Records limit
            
        Returns:
            List[LogEntry]: List of log entry instances
        """
        return await self.repository.get_all(db, skip=skip, limit=limit)
    
    async def create(self, db: AsyncIOMotorDatabase, *, obj_in: LogEntry) -> LogEntry:
        """
        Create log entry.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            obj_in (LogEntry): Input log entry
            
        Returns:
            LogEntry: Created log entry instance
        """
        return await self.repository.create(db, obj_in=obj_in)
    
    async def update(self, db: AsyncIOMotorDatabase, *, log_id: str, obj_in: Dict[str, Any]) -> Optional[LogEntry]:
        """
        Update log entry.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            log_id (str): Log entry ID
            obj_in (Dict[str, Any]): Input data
            
        Returns:
            Optional[LogEntry]: Updated log entry instance or None
        """
        obj_in["updated_at"] = datetime.utcnow()
        return await self.repository.update(db, id=log_id, obj_in=obj_in)
    
    async def delete(self, db: AsyncIOMotorDatabase, *, log_id: str) -> bool:
        """
        Delete log entry.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            log_id (str): Log entry ID
            
        Returns:
            bool: True if log entry was deleted, False otherwise
        """
        return await self.repository.delete(db, id=log_id)
