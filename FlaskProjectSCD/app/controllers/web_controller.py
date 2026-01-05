from flask import Blueprint, render_template, redirect, url_for

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    """Home page - redirect to dashboard"""
    return redirect(url_for('web.dashboard'))


@web_bp.route('/login')
def login():
    """Login page"""
    return render_template('auth/login.html')


@web_bp.route('/register')
def register():
    """Registration page"""
    return render_template('auth/register.html')


@web_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@web_bp.route('/products')
def products():
    """Products listing page"""
    return render_template('products.html')


@web_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    return render_template('product_detail.html', product_id=product_id)


@web_bp.route('/categories')
def categories():
    """Categories page"""
    return render_template('categories.html')


@web_bp.route('/suppliers')
def suppliers():
    """Suppliers page"""
    return render_template('suppliers.html')


@web_bp.route('/sales')
def sales():
    """Sales page"""
    return render_template('sales.html')


@web_bp.route('/inventory')
def inventory():
    """Inventory page"""
    return render_template('inventory.html')


@web_bp.route('/profile')
def profile():
    """User profile page"""
    return render_template('profile.html')


@web_bp.route('/reports')
def reports():
    """Reports page"""
    return render_template('reports.html')