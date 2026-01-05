from datetime import datetime
from .. import db


class User(db.Model):
    """
    User model representing system users
    Follows Single Responsibility Principle - handles only user data
    """
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(
        db.Enum('admin', 'manager', 'staff', name='user_roles'),
        nullable=False,
        default='staff'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    products_created = db.relationship(
        'Product', 
        backref='creator', 
        lazy='dynamic',
        foreign_keys='Product.created_by'
    )
    inventory_transactions = db.relationship(
        'InventoryTransaction',
        backref='user',
        lazy='dynamic'
    )
    sales = db.relationship('Sale', backref='salesperson', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'user_id': self.user_id,
            'firebase_uid': self.firebase_uid,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def has_permission(self, required_role):
        """Check if user has required permission level"""
        role_hierarchy = {'staff': 1, 'manager': 2, 'admin': 3}
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)