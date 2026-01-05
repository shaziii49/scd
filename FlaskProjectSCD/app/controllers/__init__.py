from .auth_controller import auth_bp
from .product_controller import product_bp
from .category_controller import category_bp
from .supplier_controller import supplier_bp
from .sales_controller import sales_bp

__all__ = [
    'auth_bp',
    'product_bp',
    'category_bp',
    'supplier_bp',
    'sales_bp'
]