"""
User service module.
"""
from typing import List, Optional

from sqlmodel.ext.asyncio.session import AsyncSession as Session

from app.db.repositories.user import UserRepository
from app.models.user import User, UserCreate, UserUpdate
from app.utils.security import get_password_hash, verify_password


class UserService:
    """
    User service.
    """
    def __init__(self, repository: UserRepository):
        """
        Initialize service.
        
        Args:
            repository (UserRepository): User repository
        """
        self.repository = repository
    
    async def get(self, db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db (Session): Database session
            user_id (int): User ID
            
        Returns:
            Optional[User]: User instance or None
        """
        return await self.repository.get(db, user_id)
    
    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db (Session): Database session
            email (str): User email
            
        Returns:
            Optional[User]: User instance or None
        """
        return await self.repository.get_by_email(db, email)
    
    async def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users.
        
        Args:
            db (Session): Database session
            skip (int): Records to skip
            limit (int): Records limit
            
        Returns:
            List[User]: List of user instances
        """
        return await self.repository.get_all(db, skip=skip, limit=limit)
    
    async def create(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Create user.
        
        Args:
            db (Session): Database session
            user_in (UserCreate): Input user
            
        Returns:
            User: Created user instance
        """
        # Set hashed_password in the repository
        hashed_password = get_password_hash(user_in.password)
        user_in_with_hashed = UserCreate(**user_in.model_dump())
        user_in_with_hashed.hashed_password = hashed_password
        return await self.repository.create(db, obj_in=user_in_with_hashed)
    
    async def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Update user.
        
        Args:
            db (Session): Database session
            db_obj (User): Database user
            obj_in (UserUpdate): Input user
            
        Returns:
            User: Updated user instance
        """
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)
    
    async def delete(self, db: Session, *, user_id: int) -> Optional[User]:
        """
        Delete user.
        
        Args:
            db (Session): Database session
            user_id (int): User ID
            
        Returns:
            Optional[User]: Deleted user instance or None
        """
        return await self.repository.delete(db, id=user_id)
    
    async def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate user.
        
        Args:
            db (Session): Database session
            email (str): User email
            password (str): User password
            
        Returns:
            Optional[User]: Authenticated user instance or None
        """
        user = await self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
