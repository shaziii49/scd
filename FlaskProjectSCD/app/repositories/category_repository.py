from typing import Optional, List
from ..models.category import Category
from .base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Category repository with specific category operations
    """
    
    def __init__(self):
        super().__init__(Category)
    
    def get_by_name(self, category_name: str) -> Optional[Category]:
        """Get category by name"""
        return self.model.query.filter_by(category_name=category_name).first()
    
    def name_exists(self, category_name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if category name exists"""
        query = self.model.query.filter_by(category_name=category_name)
        if exclude_id:
            query = query.filter(Category.category_id != exclude_id)
        return query.first() is not None
    
    def get_root_categories(self) -> List[Category]:
        """Get all root categories (no parent)"""
        return self.model.query.filter_by(parent_category_id=None).all()
    
    def get_subcategories(self, parent_id: int) -> List[Category]:
        """Get all subcategories of a parent category"""
        return self.model.query.filter_by(parent_category_id=parent_id).all()