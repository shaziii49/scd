from typing import Optional, List
from datetime import datetime
from ..models.sales import Sale
from .base_repository import BaseRepository
from .. import db


class SalesRepository(BaseRepository[Sale]):
    """
    Sales repository with specific sales operations
    """
    
    def __init__(self):
        super().__init__(Sale)
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime, 
                          page: int = 1, per_page: int = 20) -> tuple:
        """Get sales within a date range"""
        query = self.model.query.filter(
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        ).order_by(Sale.sale_date.desc())
        
        total = query.count()
        items = query.paginate(page=page, per_page=per_page, error_out=False).items
        
        return items, total
    
    def get_by_product(self, product_id: int, page: int = 1, per_page: int = 20) -> tuple:
        """Get sales by product"""
        return self.get_all(filters={'product_id': product_id}, page=page, per_page=per_page)
    
    def get_total_sales(self, start_date: Optional[datetime] = None, 
                       end_date: Optional[datetime] = None) -> float:
        """Calculate total sales amount"""
        query = db.session.query(db.func.sum(Sale.total_amount))
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        
        result = query.scalar()
        return float(result) if result else 0.0