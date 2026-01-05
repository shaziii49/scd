from typing import Optional
from ..models.supplier import Supplier
from .base_repository import BaseRepository
from .. import db


class SupplierRepository(BaseRepository[Supplier]):
    """
    Supplier repository with specific supplier operations
    """
    
    def __init__(self):
        super().__init__(Supplier)
    
    def get_by_name(self, supplier_name: str) -> Optional[Supplier]:
        """Get supplier by name"""
        return self.model.query.filter_by(supplier_name=supplier_name).first()
    
    def search_suppliers(self, search_term: str, page: int = 1, per_page: int = 20) -> tuple:
        """Search suppliers by name, contact person, or email"""
        query = self.model.query.filter(
            db.or_(
                Supplier.supplier_name.ilike(f'%{search_term}%'),
                Supplier.contact_person.ilike(f'%{search_term}%'),
                Supplier.email.ilike(f'%{search_term}%')
            )
        )
        
        total = query.count()
        items = query.paginate(page=page, per_page=per_page, error_out=False).items
        
        return items, total