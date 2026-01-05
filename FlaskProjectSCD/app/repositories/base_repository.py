from typing import TypeVar, Generic, List, Optional, Dict, Any
from .. import db

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository implementing common CRUD operations
    Follows Repository Pattern and Open/Closed Principle
    """
    
    def __init__(self, model: T):
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new entity"""
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        return self.model.query.get(entity_id)
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None, 
                page: int = 1, per_page: int = 20) -> tuple:
        """
        Get all entities with optional filters and pagination
        Returns: (items, total_count)
        """
        query = self.model.query
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        
        total = query.count()
        items = query.paginate(page=page, per_page=per_page, error_out=False).items
        
        return items, total
    
    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Update an entity"""
        instance = self.get_by_id(entity_id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        db.session.commit()
        return instance
    
    def delete(self, entity_id: int) -> bool:
        """Delete an entity"""
        instance = self.get_by_id(entity_id)
        if not instance:
            return False
        
        db.session.delete(instance)
        db.session.commit()
        return True
    
    def exists(self, **kwargs) -> bool:
        """Check if entity exists with given criteria"""
        query = self.model.query
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities with optional filters"""
        query = self.model.query
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.count()