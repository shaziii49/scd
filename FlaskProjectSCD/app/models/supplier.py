from datetime import datetime
from .. import db


class Supplier(db.Model):
    """
    Supplier model for managing product suppliers
    """
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(150), nullable=False, index=True)
    contact_person = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Supplier {self.supplier_name}>'
    
    def to_dict(self, include_products_count=False):
        """Convert supplier to dictionary"""
        data = {
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        return data