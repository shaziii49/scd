from typing import Optional
from ..models.user import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository with specific user operations
    Extends BaseRepository following Open/Closed Principle
    """
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """Get user by Firebase UID"""
        return self.model.query.filter_by(firebase_uid=firebase_uid).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.model.query.filter_by(email=email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.model.query.filter_by(username=username).first()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.exists(email=email)
    
    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return self.exists(username=username)
    
    def get_active_users(self, page: int = 1, per_page: int = 20) -> tuple:
        """Get all active users"""
        return self.get_all(filters={'is_active': True}, page=page, per_page=per_page)
    
    def get_users_by_role(self, role: str, page: int = 1, per_page: int = 20) -> tuple:
        """Get users by role"""
        return self.get_all(filters={'role': role}, page=page, per_page=per_page)
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user"""
        return self.update(user_id, is_active=False)
    
    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate a user"""
        return self.update(user_id, is_active=True)