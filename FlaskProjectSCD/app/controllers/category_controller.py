from flask import Blueprint, request
from ..services.category_service import CategoryService
from ..utils.response_handler import ResponseHandler
from ..middleware.auth_middleware import token_required, role_required

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')
category_service = CategoryService()


@category_bp.route('', methods=['GET'])
@token_required
def get_categories():
    """
    Get all categories with pagination
    Query params: page, per_page
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        categories, total = category_service.get_all_categories(page, per_page)
        categories_data = [c.to_dict(include_parent=True, include_subcategories=True) for c in categories]
        
        return ResponseHandler.paginated(
            categories_data, total, page, per_page,
            "Categories retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get categories: {str(e)}", 500)


@category_bp.route('/<int:category_id>', methods=['GET'])
@token_required
def get_category(category_id):
    """Get category by ID"""
    try:
        category = category_service.get_category(category_id)
        
        if not category:
            return ResponseHandler.not_found("Category not found")
        
        return ResponseHandler.success(
            category.to_dict(include_parent=True, include_subcategories=True),
            "Category retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get category: {str(e)}", 500)


@category_bp.route('', methods=['POST'])
@role_required('admin', 'manager')
def create_category():
    """
    Create a new category
    Request body: {
        "category_name": "Electronics",
        "description": "Electronic items",
        "parent_category_id": 1  (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'category_name' not in data:
            return ResponseHandler.bad_request("category_name is required")
        
        category = category_service.create_category(data)
        
        return ResponseHandler.created(
            category.to_dict(include_parent=True),
            "Category created successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to create category: {str(e)}", 500)


@category_bp.route('/<int:category_id>', methods=['PUT'])
@role_required('admin', 'manager')
def update_category(category_id):
    """Update category"""
    try:
        data = request.get_json()
        
        category = category_service.update_category(category_id, data)
        
        if not category:
            return ResponseHandler.not_found("Category not found")
        
        return ResponseHandler.success(
            category.to_dict(include_parent=True),
            "Category updated successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to update category: {str(e)}", 500)


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@role_required('admin')
def delete_category(category_id):
    """Delete category"""
    try:
        success = category_service.delete_category(category_id)
        
        if not success:
            return ResponseHandler.not_found("Category not found")
        
        return ResponseHandler.success(
            None,
            "Category deleted successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to delete category: {str(e)}", 500)


@category_bp.route('/root', methods=['GET'])
@token_required
def get_root_categories():
    """Get all root categories (no parent)"""
    try:
        categories = category_service.get_root_categories()
        categories_data = [c.to_dict(include_subcategories=True) for c in categories]
        
        return ResponseHandler.success(
            categories_data,
            "Root categories retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get root categories: {str(e)}", 500)