"""
User repository module.
"""
from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession as Session
from sqlmodel import select
from app.db.repositories.base import SQLModelRepository
from app.models.user import User, UserCreate, UserUpdate


class UserRepository(SQLModelRepository[User]):
    """
    User repository.
    """
    def __init__(self):
        """
        Initialize repository.
        """
        super().__init__(User)
        
    async def get(self, db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        """
        statement = select(User).where(User.id == user_id)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        statement = select(User).where(User.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        """
        statement = select(User).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())
        
    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user.
        """
        user_data = obj_in.model_dump(exclude={"password"})
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Update an existing user.
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, *, id: int) -> Optional[User]:
        """
        Delete a user by ID.
        """
        user = await self.get(db, id)
        if user:
            await db.delete(user)
            await db.commit()
        return user
