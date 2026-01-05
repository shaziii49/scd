from typing import Optional, Dict, Any
from ..repositories.supplier_repository import SupplierRepository
from ..models.supplier import Supplier


class SupplierService:
    """
    Supplier service handling business logic
    """
    
    def __init__(self):
        self.supplier_repository = SupplierRepository()
    
    def create_supplier(self, supplier_data: Dict[str, Any]) -> Supplier:
        """Create a new supplier"""
        return self.supplier_repository.create(**supplier_data)
    
    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """Get supplier by ID"""
        return self.supplier_repository.get_by_id(supplier_id)
    
    def get_all_suppliers(self, page: int = 1, per_page: int = 20) -> tuple:
        """Get all suppliers with pagination"""
        return self.supplier_repository.get_all(page=page, per_page=per_page)
    
    def update_supplier(self, supplier_id: int, update_data: Dict[str, Any]) -> Optional[Supplier]:
        """Update supplier"""
        supplier = self.supplier_repository.get_by_id(supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")
        
        return self.supplier_repository.update(supplier_id, **update_data)
    
    def delete_supplier(self, supplier_id: int) -> bool:
        """Delete supplier"""
        supplier = self.supplier_repository.get_by_id(supplier_id)
        if not supplier:
            raise ValueError("Supplier not found")
        
        return self.supplier_repository.delete(supplier_id)
    
    def search_suppliers(self, search_term: str, page: int = 1, per_page: int = 20) -> tuple:
        """Search suppliers"""
        return self.supplier_repository.search_suppliers(search_term, page, per_page)