"""
Log routes module.
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_mongodb
from app.db.repositories.log_entry import LogEntryRepository
from app.models.document import LogEntry
from app.services.log_entry import LogEntryService

router = APIRouter()
log_repository = LogEntryRepository()
log_service = LogEntryService(log_repository)


@router.get("/", response_model=List[LogEntry])
async def read_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """
    Get all logs.
    
    Args:
        skip (int): Records to skip
        limit (int): Records limit
        db (AsyncIOMotorDatabase): Database
        
    Returns:
        List[LogEntry]: List of logs
    """
    logs = await log_service.get_all(db, skip=skip, limit=limit)
    return logs


@router.post("/", response_model=LogEntry, status_code=status.HTTP_201_CREATED)
async def create_log(
    log_in: LogEntry,
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """
    Create log.
    
    Args:
        log_in (LogEntry): Input log
        db (AsyncIOMotorDatabase): Database
        
    Returns:
        LogEntry: Created log
    """
    log = await log_service.create(db, obj_in=log_in)
    return log


@router.get("/{log_id}", response_model=LogEntry)
async def read_log(
    log_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """
    Get log by ID.
    
    Args:
        log_id (str): Log ID
        db (AsyncIOMotorDatabase): Database
        
    Returns:
        LogEntry: Log
    """
    log = await log_service.get(db, log_id=log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found",
        )
    return log


@router.put("/{log_id}", response_model=LogEntry)
async def update_log(
    log_id: str,
    log_in: Dict[str, Any],
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """
    Update log.
    
    Args:
        log_id (str): Log ID
        log_in (Dict[str, Any]): Input log
        db (AsyncIOMotorDatabase): Database
        
    Returns:
        LogEntry: Updated log
    """
    log = await log_service.get(db, log_id=log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found",
        )
    log = await log_service.update(db, log_id=log_id, obj_in=log_in)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """
    Delete log.
    
    Args:
        log_id (str): Log ID
        db (AsyncIOMotorDatabase): Database
    """
    log = await log_service.get(db, log_id=log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found",
        )
    deleted = await log_service.delete(db, log_id=log_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete log",
        )
