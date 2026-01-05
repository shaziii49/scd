from datetime import datetime
from .. import db


class Category(db.Model):
    """
    Category model for product categorization
    Supports hierarchical categories (parent-child relationship)
    """
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    parent_category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.category_id', ondelete='SET NULL'),
        nullable=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Self-referential relationship for hierarchical categories
    subcategories = db.relationship(
        'Category',
        backref=db.backref('parent', remote_side=[category_id]),
        lazy='dynamic'
    )
    
    # Relationship with products
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.category_name}>'
    
    def to_dict(self, include_parent=True, include_subcategories=False):
        """Convert category to dictionary"""
        data = {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'description': self.description,
            'parent_category_id': self.parent_category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_parent and self.parent:
            data['parent_category'] = {
                'category_id': self.parent.category_id,
                'category_name': self.parent.category_name
            }
        
        if include_subcategories:
            data['subcategories'] = [
                {
                    'category_id': sub.category_id,
                    'category_name': sub.category_name
                }
                for sub in self.subcategories.all()
            ]
        
        return data
    
    def get_full_path(self):
        """Get full category path (e.g., 'Electronics > Computers > Laptops')"""
        path = [self.category_name]
        current = self.parent
        while current:
            path.insert(0, current.category_name)
            current = current.parent
        return ' > '.join(path)