from typing import Optional, Dict, Any
from datetime import datetime
from ..repositories.sales_repository import SalesRepository
from ..repositories.product_repository import ProductRepository
from ..models.sales import Sale


class SalesService:
    """
    Sales service handling business logic
    """
    
    def __init__(self):
        self.sales_repository = SalesRepository()
        self.product_repository = ProductRepository()
    
    def create_sale(self, sale_data: Dict[str, Any], user_id: int) -> Sale:
        """Create a new sale and update inventory"""
        # Validate product exists
        product = self.product_repository.get_by_id(sale_data['product_id'])
        if not product:
            raise ValueError("Product not found")
        
        # Check stock availability
        if product.quantity_in_stock < sale_data['quantity_sold']:
            raise ValueError(f"Insufficient stock. Available: {product.quantity_in_stock}")
        
        # Calculate total amount if not provided or is None/empty
        if 'total_amount' not in sale_data or sale_data['total_amount'] is None or sale_data['total_amount'] == '':
            sale_data['total_amount'] = sale_data['quantity_sold'] * sale_data['unit_price']
        
        # Add user_id
        sale_data['user_id'] = user_id
        
        # Create sale
        sale = self.sales_repository.create(**sale_data)
        
        # Update product stock
        self.product_repository.update_stock(
            sale_data['product_id'], 
            -sale_data['quantity_sold']
        )
        
        return sale
    
    def get_sale(self, sale_id: int) -> Optional[Sale]:
        """Get sale by ID"""
        return self.sales_repository.get_by_id(sale_id)
    
    def get_all_sales(self, page: int = 1, per_page: int = 20) -> tuple:
        """Get all sales with pagination"""
        return self.sales_repository.get_all(page=page, per_page=per_page)
    
    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime,
                                page: int = 1, per_page: int = 20) -> tuple:
        """Get sales within date range"""
        return self.sales_repository.get_by_date_range(start_date, end_date, page, per_page)
    
    def get_total_sales(self, start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> float:
        """Get total sales amount"""
        return self.sales_repository.get_total_sales(start_date, end_date)
    
    def delete_sale(self, sale_id: int) -> bool:
        """Delete a sale"""
        sale = self.sales_repository.get_by_id(sale_id)
        if not sale:
            raise ValueError("Sale not found")
        
        # Restore product stock when deleting a sale
        self.product_repository.update_stock(
            sale.product_id, 
            sale.quantity_sold  # Add back the quantity that was sold
        )
        
        return self.sales_repository.delete(sale_id)