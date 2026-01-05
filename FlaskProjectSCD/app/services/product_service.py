from typing import Optional, List, Dict, Any
from ..repositories.product_repository import ProductRepository
from ..models.product import Product


class ProductService:
    """
    Product service handling business logic
    Follows Single Responsibility Principle
    """
    
    def __init__(self):
        self.product_repository = ProductRepository()
    
    def create_product(self, product_data: Dict[str, Any], created_by: int) -> Product:
        """Create a new product"""
        # Validate SKU uniqueness
        if self.product_repository.sku_exists(product_data['sku']):
            raise ValueError("SKU already exists")
        
        # Validate price
        if product_data.get('price', 0) <= 0:
            raise ValueError("Price must be greater than 0")
        
        # Add creator
        product_data['created_by'] = created_by
        
        return self.product_repository.create(**product_data)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.product_repository.get_by_id(product_id)
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        return self.product_repository.get_by_sku(sku)
    
    def get_all_products(self, page: int = 1, per_page: int = 20, 
                         active_only: bool = True) -> tuple:
        """Get all products with pagination"""
        if active_only:
            return self.product_repository.get_active_products(page, per_page)
        return self.product_repository.get_all(page=page, per_page=per_page)
    
    def update_product(self, product_id: int, update_data: Dict[str, Any]) -> Optional[Product]:
        """Update product"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Validate SKU if being updated
        if 'sku' in update_data and update_data['sku'] != product.sku:
            if self.product_repository.sku_exists(update_data['sku'], exclude_id=product_id):
                raise ValueError("SKU already exists")
        
        # Validate price if being updated
        if 'price' in update_data and update_data['price'] <= 0:
            raise ValueError("Price must be greater than 0")
        
        return self.product_repository.update(product_id, **update_data)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product (hard delete from database)"""
        return self.product_repository.delete(product_id)
    
    def search_products(self, search_term: str, page: int = 1, 
                       per_page: int = 20) -> tuple:
        """Search products"""
        return self.product_repository.search_products(search_term, page, per_page)
    
    def get_products_by_category(self, category_id: int, page: int = 1, 
                                 per_page: int = 20) -> tuple:
        """Get products by category"""
        return self.product_repository.get_by_category(category_id, page, per_page)
    
    def get_products_by_supplier(self, supplier_id: int, page: int = 1, 
                                 per_page: int = 20) -> tuple:
        """Get products by supplier"""
        return self.product_repository.get_by_supplier(supplier_id, page, per_page)
    
    def get_low_stock_products(self) -> List[Product]:
        """Get products with stock below reorder level"""
        return self.product_repository.get_low_stock_products()
    
    def update_stock(self, product_id: int, quantity_change: int) -> Product:
        """Update product stock"""
        try:
            return self.product_repository.update_stock(product_id, quantity_change)
        except ValueError as e:
            raise ValueError(str(e))
    
    def get_inventory_value(self) -> float:
        """Get total inventory value"""
        return self.product_repository.get_inventory_value()