from datetime import datetime
from .. import db


class InventoryTransaction(db.Model):
    """
    Inventory transaction model for tracking stock movements
    """
    __tablename__ = 'inventory_transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.product_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    transaction_type = db.Column(
        db.Enum('IN', 'OUT', 'ADJUSTMENT', name='transaction_types'),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete='SET NULL'),
        nullable=True
    )
    notes = db.Column(db.Text, nullable=True)
    reference_number = db.Column(db.String(50), nullable=True, index=True)
    
    def __repr__(self):
        return f'<InventoryTransaction {self.transaction_id} - {self.transaction_type}>'
    
    def to_dict(self, include_relations=False):
        """Convert inventory transaction to dictionary"""
        data = {
            'transaction_id': self.transaction_id,
            'product_id': self.product_id,
            'transaction_type': self.transaction_type,
            'quantity': self.quantity,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'user_id': self.user_id,
            'notes': self.notes,
            'reference_number': self.reference_number
        }
        
        if include_relations:
            if self.product:
                data['product'] = {
                    'product_id': self.product.product_id,
                    'product_name': self.product.product_name,
                    'sku': self.product.sku
                }
            if self.user:
                data['user'] = {
                    'user_id': self.user.user_id,
                    'username': self.user.username,
                    'full_name': self.user.full_name
                }
        
        return data