from datetime import datetime
from .. import db


class Product(db.Model):
    """
    Product model representing items in inventory
    """
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(200), nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.category_id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0.00
    )
    cost_price = db.Column(db.Numeric(10, 2), nullable=True)
    quantity_in_stock = db.Column(db.Integer, default=0, nullable=False)
    reorder_level = db.Column(db.Integer, default=10, nullable=False)
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey('suppliers.supplier_id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    image_url = db.Column(db.String(255), nullable=True)
    barcode = db.Column(db.String(100), unique=True, nullable=True)
    weight = db.Column(db.Numeric(8, 2), nullable=True)
    dimensions = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete='SET NULL'),
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    inventory_transactions = db.relationship(
        'InventoryTransaction',
        backref='product',
        lazy='dynamic'
    )
    sales = db.relationship('Sale', backref='product', lazy='dynamic')
    
    # Check constraints
    __table_args__ = (
        db.CheckConstraint('price > 0', name='check_price_positive'),
        db.CheckConstraint('quantity_in_stock >= 0', name='check_quantity_non_negative'),
    )
    
    def __repr__(self):
        return f'<Product {self.product_name}>'
    
    def to_dict(self, include_relations=False):
        """Convert product to dictionary"""
        data = {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'sku': self.sku,
            'description': self.description,
            'category_id': self.category_id,
            'price': float(self.price) if self.price else 0.0,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'quantity_in_stock': self.quantity_in_stock,
            'reorder_level': self.reorder_level,
            'supplier_id': self.supplier_id,
            'image_url': self.image_url,
            'barcode': self.barcode,
            'weight': float(self.weight) if self.weight else None,
            'dimensions': self.dimensions,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            if self.category:
                data['category'] = {
                    'category_id': self.category.category_id,
                    'category_name': self.category.category_name
                }
            if self.supplier:
                data['supplier'] = {
                    'supplier_id': self.supplier.supplier_id,
                    'supplier_name': self.supplier.supplier_name
                }
            if self.creator:
                data['created_by_user'] = {
                    'user_id': self.creator.user_id,
                    'username': self.creator.username
                }
        
        return data
    
    def is_low_stock(self):
        """Check if product is below reorder level"""
        return self.quantity_in_stock <= self.reorder_level
    
    def get_profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.cost_price > 0:
            return ((self.price - self.cost_price) / self.cost_price) * 100
        return None