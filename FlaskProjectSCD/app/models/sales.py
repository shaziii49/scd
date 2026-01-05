from datetime import datetime
from .. import db


class Sale(db.Model):
    """
    Sales model for recording product sales
    """
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.product_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    quantity_sold = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    customer_name = db.Column(db.String(100), nullable=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete='SET NULL'),
        nullable=True
    )
    
    # Relationships
    # Note: product relationship is defined in Product model with backref='product'
    
    # Check constraints
    __table_args__ = (
        db.CheckConstraint('quantity_sold > 0', name='check_quantity_positive'),
    )
    
    def __repr__(self):
        return f'<Sale {self.sale_id}>'
    
    def to_dict(self, include_relations=False):
        """Convert sale to dictionary"""
        data = {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity_sold': self.quantity_sold,
            'unit_price': float(self.unit_price) if self.unit_price else 0.0,
            'total_amount': float(self.total_amount) if self.total_amount else 0.0,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'customer_name': self.customer_name,
            'user_id': self.user_id
        }
        
        if include_relations:
            if self.product:
                data['product'] = {
                    'product_id': self.product.product_id,
                    'product_name': self.product.product_name,
                    'sku': self.product.sku
                }
            if self.salesperson:
                data['salesperson'] = {
                    'user_id': self.salesperson.user_id,
                    'username': self.salesperson.username,
                    'full_name': self.salesperson.full_name
                }
        
        return data