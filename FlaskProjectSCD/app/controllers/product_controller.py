from flask import Blueprint, request, g
from ..services.product_service import ProductService
from ..utils.response_handler import ResponseHandler
from ..middleware.auth_middleware import token_required, role_required

product_bp = Blueprint('products', __name__, url_prefix='/api/products')
product_service = ProductService()


@product_bp.route('', methods=['GET'])
@token_required
def get_products():
    """
    Get all products with pagination
    Query params: page, per_page, active_only, search, category_id, status
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        search = request.args.get('search', None)
        category_id = request.args.get('category_id', None, type=int)
        status = request.args.get('status', None)
        
        if search:
            products, total = product_service.search_products(search, page, per_page)
        elif category_id:
            products, total = product_service.get_products_by_category(category_id, page, per_page)
        elif status == 'low_stock':
            # For low stock, get all products and filter client-side or modify service
            all_products = product_service.get_low_stock_products()
            # Simple pagination for low stock (could be improved)
            start = (page - 1) * per_page
            end = start + per_page
            products = all_products[start:end]
            total = len(all_products)
        else:
            products, total = product_service.get_all_products(page, per_page, active_only)
        
        products_data = [p.to_dict(include_relations=True) for p in products]
        
        return ResponseHandler.paginated(
            products_data, total, page, per_page,
            "Products retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get products: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['GET'])
@token_required
def get_product(product_id):
    """Get product by ID"""
    try:
        product = product_service.get_product(product_id)
        
        if not product:
            return ResponseHandler.not_found("Product not found")
        
        return ResponseHandler.success(
            product.to_dict(include_relations=True),
            "Product retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get product: {str(e)}", 500)


@product_bp.route('', methods=['POST'])
@role_required('admin', 'manager')
def create_product():
    """
    Create a new product
    Request body: {
        "product_name": "Laptop",
        "sku": "LAP001",
        "description": "Gaming laptop",
        "category_id": 1,
        "price": 1500.00,
        "cost_price": 1200.00,
        "quantity_in_stock": 10,
        "reorder_level": 5,
        "supplier_id": 1
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_name', 'sku', 'price']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return ResponseHandler.bad_request(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        user = g.current_user
        product = product_service.create_product(data, user.user_id)
        
        return ResponseHandler.created(
            product.to_dict(include_relations=True),
            "Product created successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to create product: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['PUT'])
@role_required('admin', 'manager')
def update_product(product_id):
    """Update product"""
    try:
        data = request.get_json()
        
        product = product_service.update_product(product_id, data)
        
        if not product:
            return ResponseHandler.not_found("Product not found")
        
        return ResponseHandler.success(
            product.to_dict(include_relations=True),
            "Product updated successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to update product: {str(e)}", 500)


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@role_required('admin')
def delete_product(product_id):
    """Delete product (hard delete)"""
    try:
        success = product_service.delete_product(product_id)
        
        if not success:
            return ResponseHandler.not_found("Product not found")
        
        return ResponseHandler.success(
            None,
            "Product deleted successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to delete product: {str(e)}", 500)


@product_bp.route('/low-stock', methods=['GET'])
@token_required
def get_low_stock_products():
    """Get products with low stock"""
    try:
        products = product_service.get_low_stock_products()
        products_data = [p.to_dict(include_relations=True) for p in products]
        
        return ResponseHandler.success(
            products_data,
            "Low stock products retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get low stock products: {str(e)}", 500)


@product_bp.route('/inventory-value', methods=['GET'])
@role_required('admin', 'manager')
def get_inventory_value():
    """Get total inventory value"""
    try:
        value = product_service.get_inventory_value()
        
        return ResponseHandler.success(
            {'inventory_value': value},
            "Inventory value calculated successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to calculate inventory value: {str(e)}", 500)


@product_bp.route('/<int:product_id>/stock', methods=['PUT'])
@role_required('admin', 'manager')
def update_stock(product_id):
    """
    Update product stock
    Request body: {
        "quantity_change": 10  (positive for add, negative for subtract)
    }
    """
    try:
        data = request.get_json()
        
        if 'quantity_change' not in data:
            return ResponseHandler.bad_request("quantity_change is required")
        
        product = product_service.update_stock(product_id, data['quantity_change'])
        
        return ResponseHandler.success(
            product.to_dict(include_relations=True),
            "Stock updated successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to update stock: {str(e)}", 500)