"""
User model module.
"""
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin


class UserBase(SQLModel):
    """
    Base user model.
    
    Attributes:
        email (EmailStr): User email
        full_name (str): User full name
        is_active (bool): User is active flag
        is_superuser (bool): User is superuser flag
    """
    email: EmailStr = Field(unique=True, index=True)
    full_name: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, TimestampMixin, table=True):
    """
    User model.
    
    Attributes:
        id (int): User ID
        hashed_password (str): Hashed password
    """
    __tablename__: str = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    """
    User creation model.
    
    Attributes:
        password (str): Plain password
    """
    password: str
    hashed_password: str


class UserRead(UserBase):
    """
    User read model.
    
    Attributes:
        id (int): User ID
    """
    id: int


class UserUpdate(SQLModel):
    """
    User update model.
    
    Attributes:
        email (Optional[EmailStr]): User email
        full_name (Optional[str]): User full name
        is_active (Optional[bool]): User is active flag
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
