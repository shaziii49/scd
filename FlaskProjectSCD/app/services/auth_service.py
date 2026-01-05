import firebase_admin
from firebase_admin import auth, credentials
from typing import Optional, Dict
from ..repositories.user_repository import UserRepository
from ..models.user import User
import os


class AuthService:
    """
    Authentication service using Firebase
    Follows Single Responsibility Principle - handles only authentication
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern for AuthService"""
        if cls._instance is None:
            cls._instance = super(AuthService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        if not AuthService._initialized:
            try:
                firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH', 'firebase-config.json')
                if not os.path.exists(firebase_config_path):
                    raise FileNotFoundError(f"Firebase config not found at {firebase_config_path}")
                
                cred = credentials.Certificate(firebase_config_path)
                firebase_admin.initialize_app(cred)
                AuthService._initialized = True
            except ValueError:
                # Firebase already initialized
                pass
        
        self.user_repository = UserRepository()
    
    def verify_token(self, id_token: str) -> Optional[Dict]:
        """
        Verify Firebase ID token
        Returns decoded token if valid, None otherwise
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None
    
    def register_user(self, firebase_uid: str, email: str, username: str, 
                     full_name: str, role: str = 'staff') -> Optional[User]:
        """
        Register a new user after Firebase authentication
        """
        # Check if user already exists
        if self.user_repository.email_exists(email):
            raise ValueError("Email already registered")
        
        if self.user_repository.username_exists(username):
            raise ValueError("Username already taken")
        
        # Validate role
        valid_roles = ['admin', 'manager', 'staff']
        if role not in valid_roles:
            role = 'staff'
        
        # Create user in database
        user = self.user_repository.create(
            firebase_uid=firebase_uid,
            email=email,
            username=username,
            full_name=full_name,
            role=role,
            is_active=True
        )
        
        return user
    
    def login_user(self, id_token: str) -> Optional[User]:
        """
        Login user using Firebase ID token
        """
        decoded_token = self.verify_token(id_token)
        if not decoded_token:
            return None
        
        firebase_uid = decoded_token.get('uid')
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        
        if not user:
            return None
        
        if not user.is_active:
            raise ValueError("User account is deactivated")
        
        return user
    
    def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """Get user by Firebase UID"""
        return self.user_repository.get_by_firebase_uid(firebase_uid)
    
    def update_user_role(self, user_id: int, new_role: str) -> Optional[User]:
        """Update user role (admin only)"""
        valid_roles = ['admin', 'manager', 'staff']
        if new_role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        return self.user_repository.update(user_id, role=new_role)
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate user account"""
        return self.user_repository.deactivate_user(user_id)
    
    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate user account"""
        return self.user_repository.activate_user(user_id)