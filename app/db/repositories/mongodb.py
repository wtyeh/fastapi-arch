"""
MongoDB repository module.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel

from app.models.document import Document

T = TypeVar("T", bound=Document)


class MongoDBRepository(Generic[T]):
    """
    Base MongoDB repository.
    
    Attributes:
        model_class (Type[T]): Model class
        collection_name (str): Collection name
    """
    def __init__(self, model_class: Type[T], collection_name: str):
        """
        Initialize repository.
        
        Args:
            model_class (Type[T]): Model class
            collection_name (str): Collection name
        """
        self.model_class = model_class
        self.collection_name = collection_name
    
    def get_collection(self, db: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
        """
        Get collection.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            
        Returns:
            AsyncIOMotorCollection: Collection
        """
        return db[self.collection_name]
    
    async def get(self, db: AsyncIOMotorDatabase, id: str) -> Optional[T]:
        """
        Get document by ID.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            id (str): Document ID
            
        Returns:
            Optional[T]: Document instance or None
        """
        collection = self.get_collection(db)
        document = await collection.find_one({"_id": ObjectId(id)})
        if document:
            document["_id"] = str(document["_id"])
            return self.model_class(**document)
        return None
    
    async def get_all(self, db: AsyncIOMotorDatabase, *, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all documents.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            skip (int): Documents to skip
            limit (int): Documents limit
            
        Returns:
            List[T]: List of document instances
        """
        collection = self.get_collection(db)
        cursor = collection.find().skip(skip).limit(limit)
        documents = []
        async for document in cursor:
            document["_id"] = str(document["_id"])
            documents.append(self.model_class(**document))
        return documents
    
    async def create(self, db: AsyncIOMotorDatabase, *, obj_in: BaseModel) -> T:
        """
        Create document.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            obj_in (BaseModel): Input model
            
        Returns:
            T: Created document instance
        """
        collection = self.get_collection(db)
        obj_data = obj_in.model_dump(exclude={"id"})
        result = await collection.insert_one(obj_data)
        document = await collection.find_one({"_id": result.inserted_id})
        document["_id"] = str(document["_id"])
        return self.model_class(**document)
    
    async def update(self, db: AsyncIOMotorDatabase, *, id: str, obj_in: Dict[str, Any]) -> Optional[T]:
        """
        Update document.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            id (str): Document ID
            obj_in (Dict[str, Any]): Input data
            
        Returns:
            Optional[T]: Updated document instance or None
        """
        collection = self.get_collection(db)
        result = await collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": obj_in}
        )
        if result.modified_count:
            return await self.get(db, id)
        return None
    
    async def delete(self, db: AsyncIOMotorDatabase, *, id: str) -> bool:
        """
        Delete document.
        
        Args:
            db (AsyncIOMotorDatabase): Database
            id (str): Document ID
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        collection = self.get_collection(db)
        result = await collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
