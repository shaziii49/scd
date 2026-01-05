from flask import Blueprint, request, g
from datetime import datetime
from ..services.sales_service import SalesService
from ..utils.response_handler import ResponseHandler
from ..middleware.auth_middleware import token_required, role_required

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')
sales_service = SalesService()


@sales_bp.route('', methods=['GET'])
@token_required
def get_sales():
    """
    Get all sales with pagination
    Query params: page, per_page, start_date, end_date
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date and end_date:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            
            # If end_date has no time component, set it to end of day
            if end.time() == datetime.min.time():
                end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            sales, total = sales_service.get_sales_by_date_range(start, end, page, per_page)
        else:
            sales, total = sales_service.get_all_sales(page, per_page)
        
        sales_data = [s.to_dict(include_relations=True) for s in sales]
        
        return ResponseHandler.paginated(
            sales_data, total, page, per_page,
            "Sales retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get sales: {str(e)}", 500)


@sales_bp.route('/<int:sale_id>', methods=['GET'])
@token_required
def get_sale(sale_id):
    """Get sale by ID"""
    try:
        sale = sales_service.get_sale(sale_id)
        
        if not sale:
            return ResponseHandler.not_found("Sale not found")
        
        return ResponseHandler.success(
            sale.to_dict(include_relations=True),
            "Sale retrieved successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to get sale: {str(e)}", 500)


@sales_bp.route('', methods=['POST'])
@token_required
def create_sale():
    """
    Create a new sale
    Request body: {
        "product_id": 1,
        "quantity_sold": 5,
        "unit_price": 100.00,
        "customer_name": "John Doe" (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_id', 'quantity_sold', 'unit_price']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return ResponseHandler.bad_request(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        user = g.current_user
        sale = sales_service.create_sale(data, user.user_id)
        
        return ResponseHandler.created(
            sale.to_dict(include_relations=True),
            "Sale recorded successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to create sale: {str(e)}", 500)


@sales_bp.route('/total', methods=['GET'])
@token_required
def get_total_sales():
    """
    Get total sales amount
    Query params: start_date, end_date (optional)
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Parse dates - if only date provided, handle appropriately
        start = None
        end = None
        
        if start_date:
            start = datetime.fromisoformat(start_date)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
            # If end_date has no time component, set it to end of day
            if end.time() == datetime.min.time():
                end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total = sales_service.get_total_sales(start, end)
        
        return ResponseHandler.success(
            {'total_sales': total},
            "Total sales calculated successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to calculate total sales: {str(e)}", 500)


@sales_bp.route('/<int:sale_id>', methods=['DELETE'])
@role_required('admin')
def delete_sale(sale_id):
    """
    Delete a sale
    """
    try:
        success = sales_service.delete_sale(sale_id)
        
        if not success:
            return ResponseHandler.not_found("Sale not found")
        
        return ResponseHandler.success(
            None,
            "Sale deleted successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to delete sale: {str(e)}", 500)