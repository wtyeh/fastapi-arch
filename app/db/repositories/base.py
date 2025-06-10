"""
Base repository module.
"""
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class SQLModelRepository(Generic[T]):
    """
    Base SQLModel repository.
    
    Attributes:
        model_class (Type[T]): Model class
    """
    def __init__(self, model_class: Type[T]):
        """
        Initialize repository.
        
        Args:
            model_class (Type[T]): Model class
        """
        self.model_class = model_class
    
    def get(self, db: Session, id: int) -> Optional[T]:
        """
        Get model by ID.
        
        Args:
            db (Session): Database session
            id (int): Model ID
            
        Returns:
            Optional[T]: Model instance or None
        """
        return db.get(self.model_class, id)
    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all models.
        
        Args:
            db (Session): Database session
            skip (int): Records to skip
            limit (int): Records limit
            
        Returns:
            List[T]: List of model instances
        """
        statement = select(self.model_class).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return list(results)
    
    def create(self, db: Session, *, obj_in: BaseModel) -> T:
        """
        Create model.
        
        Args:
            db (Session): Database session
            obj_in (BaseModel): Input model
            
        Returns:
            T: Created model instance
        """
        obj_data = obj_in.model_dump()
        db_obj = self.model_class(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: T, obj_in: BaseModel) -> T:
        """
        Update model.
        
        Args:
            db (Session): Database session
            db_obj (T): Database model
            obj_in (BaseModel): Input model
            
        Returns:
            T: Updated model instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> Optional[T]:
        """
        Delete model.
        
        Args:
            db (Session): Database session
            id (int): Model ID
            
        Returns:
            Optional[T]: Deleted model instance or None
        """
        obj = db.get(self.model_class, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


