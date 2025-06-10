"""
User routes module.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession as Session

from app.db.postgres import get_async_session
from app.db.repositories.user import UserRepository
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter()
user_repository = UserRepository()
user_service = UserService(user_repository)


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_async_session),
):
    """
    Get all users.
    
    Args:
        skip (int): Records to skip
        limit (int): Records limit
        db (Session): Database session
        
    Returns:
        List[UserRead]: List of users
    """
    users = await user_service.get_all(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_async_session),
):
    """
    Create user.
    
    Args:
        user_in (UserCreate): Input user
        db (Session): Database session
        
    Returns:
        UserRead: Created user
    """
    user = await user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user = await user_service.create(db, user_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: Session = Depends(get_async_session),
):
    """
    Get user by ID.
    
    Args:
        user_id (int): User ID
        db (Session): Database session
        
    Returns:
        UserRead: User
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_async_session),
):
    """
    Update user.
    
    Args:
        user_id (int): User ID
        user_in (UserUpdate): Input user
        db (Session): Database session
        
    Returns:
        UserRead: Updated user
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await user_service.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_async_session),
):
    """
    Delete user.
    
    Args:
        user_id (int): User ID
        db (Session): Database session
        
    Returns:
        UserRead: Deleted user
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await user_service.delete(db, user_id=user_id)
    return user
