from typing import Optional, List
from ..models.product import Product
from .base_repository import BaseRepository
from .. import db


class ProductRepository(BaseRepository[Product]):
    """
    Product repository with specific product operations
    """
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        return self.model.query.filter_by(sku=sku).first()
    
    def sku_exists(self, sku: str, exclude_id: Optional[int] = None) -> bool:
        """Check if SKU exists (optionally exclude a product ID)"""
        query = self.model.query.filter_by(sku=sku)
        if exclude_id:
            query = query.filter(Product.product_id != exclude_id)
        return query.first() is not None
    
    def get_active_products(self, page: int = 1, per_page: int = 20) -> tuple:
        """Get all active products"""
        return self.get_all(filters={'is_active': True}, page=page, per_page=per_page)
    
    def get_by_category(self, category_id: int, page: int = 1, per_page: int = 20) -> tuple:
        """Get products by category"""
        return self.get_all(filters={'category_id': category_id}, page=page, per_page=per_page)
    
    def get_by_supplier(self, supplier_id: int, page: int = 1, per_page: int = 20) -> tuple:
        """Get products by supplier"""
        return self.get_all(filters={'supplier_id': supplier_id}, page=page, per_page=per_page)
    
    def get_low_stock_products(self) -> List[Product]:
        """Get products below reorder level"""
        return self.model.query.filter(
            Product.quantity_in_stock <= Product.reorder_level
        ).all()
    
    def search_products(self, search_term: str, page: int = 1, per_page: int = 20) -> tuple:
        """Search products by name, SKU, or description"""
        query = self.model.query.filter(
            db.or_(
                Product.product_name.ilike(f'%{search_term}%'),
                Product.sku.ilike(f'%{search_term}%'),
                Product.description.ilike(f'%{search_term}%')
            )
        )
        
        total = query.count()
        items = query.paginate(page=page, per_page=per_page, error_out=False).items
        
        return items, total
    
    def update_stock(self, product_id: int, quantity_change: int) -> Optional[Product]:
        """Update product stock quantity"""
        product = self.get_by_id(product_id)
        if not product:
            return None
        
        new_quantity = product.quantity_in_stock + quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        
        return self.update(product_id, quantity_in_stock=new_quantity)
    
    def get_inventory_value(self) -> float:
        """Calculate total inventory value"""
        result = db.session.query(
            db.func.sum(Product.quantity_in_stock * Product.cost_price)
        ).scalar()
        return float(result) if result else 0.0