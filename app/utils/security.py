"""
Security utilities module.
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password.
    
    Args:
        plain_password (str): Plain password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if password is valid, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get password hash.
    
    Args:
        password (str): Plain password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)
