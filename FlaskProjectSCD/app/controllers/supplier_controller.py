from flask import Blueprint, request
from ..services.supplier_service import SupplierService
from ..utils.response_handler import ResponseHandler
from ..middleware.auth_middleware import token_required, role_required

supplier_bp = Blueprint('suppliers', __name__, url_prefix='/api/suppliers')
supplier_service = SupplierService()


@supplier_bp.route('', methods=['GET'])
@token_required
def get_suppliers():
    """
    Get all suppliers with pagination
    Query params: page, per_page, search
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', None)
        
        if search:
            suppliers, total = supplier_service.search_suppliers(search, page, per_page)
        else:
            suppliers, total = supplier_service.get_all_suppliers(page, per_page)
        
        suppliers_data = [s.to_dict(include_products_count=True) for s in suppliers]
        
        return ResponseHandler.paginated(
            suppliers_data, total, page, per_page,
            "Suppliers retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get suppliers: {str(e)}", 500)


@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
@token_required
def get_supplier(supplier_id):
    """Get supplier by ID"""
    try:
        supplier = supplier_service.get_supplier(supplier_id)
        
        if not supplier:
            return ResponseHandler.not_found("Supplier not found")
        
        return ResponseHandler.success(
            supplier.to_dict(include_products_count=True),
            "Supplier retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get supplier: {str(e)}", 500)


@supplier_bp.route('', methods=['POST'])
@role_required('admin', 'manager')
def create_supplier():
    """
    Create a new supplier
    Request body: {
        "supplier_name": "Tech Supplies Inc",
        "contact_person": "John Doe",
        "email": "john@techsupplies.com",
        "phone": "+1234567890",
        "address": "123 Main St"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'supplier_name' not in data:
            return ResponseHandler.bad_request("supplier_name is required")
        
        supplier = supplier_service.create_supplier(data)
        
        return ResponseHandler.created(
            supplier.to_dict(),
            "Supplier created successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to create supplier: {str(e)}", 500)


@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
@role_required('admin', 'manager')
def update_supplier(supplier_id):
    """Update supplier"""
    try:
        data = request.get_json()
        
        supplier = supplier_service.update_supplier(supplier_id, data)
        
        if not supplier:
            return ResponseHandler.not_found("Supplier not found")
        
        return ResponseHandler.success(
            supplier.to_dict(),
            "Supplier updated successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to update supplier: {str(e)}", 500)


@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
@role_required('admin')
def delete_supplier(supplier_id):
    """Delete supplier"""
    try:
        success = supplier_service.delete_supplier(supplier_id)
        
        if not success:
            return ResponseHandler.not_found("Supplier not found")
        
        return ResponseHandler.success(
            None,
            "Supplier deleted successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to delete supplier: {str(e)}", 500)