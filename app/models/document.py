"""
MongoDB document models module.
"""
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Base document model.
    
    Attributes:
        id (Optional[str]): Document ID
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """
        Pydantic model configuration.
        """
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


class LogEntry(Document):
    """
    Log entry model.
    
    Attributes:
        level (str): Log level
        message (str): Log message
        service (str): Service name
        metadata (Dict): Additional metadata
        tags (List[str]): Tags
    """
    level: str
    message: str
    service: str
    metadata: Dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
