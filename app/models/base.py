"""
Base models module for SQLModel models.
"""
from datetime import datetime
from typing import Optional

from pydantic import Field
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """
    Timestamp mixin for models.
    
    Attributes:
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
