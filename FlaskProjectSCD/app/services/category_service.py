from typing import Optional, List, Dict, Any
from ..repositories.category_repository import CategoryRepository
from ..models.category import Category


class CategoryService:
    """
    Category service handling business logic
    """
    
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    def create_category(self, category_data: Dict[str, Any]) -> Category:
        """Create a new category"""
        # Validate name uniqueness
        if self.category_repository.name_exists(category_data['category_name']):
            raise ValueError("Category name already exists")
        
        # Validate parent category if provided
        if category_data.get('parent_category_id'):
            parent = self.category_repository.get_by_id(category_data['parent_category_id'])
            if not parent:
                raise ValueError("Parent category not found")
        
        return self.category_repository.create(**category_data)
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.category_repository.get_by_id(category_id)
    
    def get_all_categories(self, page: int = 1, per_page: int = 20) -> tuple:
        """Get all categories with pagination"""
        return self.category_repository.get_all(page=page, per_page=per_page)
    
    def get_root_categories(self) -> List[Category]:
        """Get all root categories"""
        return self.category_repository.get_root_categories()
    
    def update_category(self, category_id: int, update_data: Dict[str, Any]) -> Optional[Category]:
        """Update category"""
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        
        # Validate name if being updated
        if 'category_name' in update_data and update_data['category_name'] != category.category_name:
            if self.category_repository.name_exists(update_data['category_name'], exclude_id=category_id):
                raise ValueError("Category name already exists")
        
        return self.category_repository.update(category_id, **update_data)
    
    def delete_category(self, category_id: int) -> bool:
        """Delete category"""
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        
        # Check if category has subcategories
        subcategories = self.category_repository.get_subcategories(category_id)
        if subcategories:
            raise ValueError("Cannot delete category with subcategories")
        
        return self.category_repository.delete(category_id)