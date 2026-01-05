from flask import Blueprint, request, g
from ..services.auth_service import AuthService
from ..utils.response_handler import ResponseHandler
from ..middleware.auth_middleware import token_required, role_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    Request body: {
        "id_token": "firebase_id_token",
        "username": "johndoe",
        "full_name": "John Doe",
        "role": "staff" (optional, defaults to staff)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id_token', 'username', 'full_name']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return ResponseHandler.bad_request(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Verify Firebase token first
        id_token = data['id_token']
        decoded_token = auth_service.verify_token(id_token)
        
        if not decoded_token:
            return ResponseHandler.unauthorized("Invalid Firebase token")
        
        # Extract Firebase UID and email
        firebase_uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        
        if not email:
            return ResponseHandler.bad_request("Email not found in Firebase token")
        
        # Register user
        user = auth_service.register_user(
            firebase_uid=firebase_uid,
            email=email,
            username=data['username'],
            full_name=data['full_name'],
            role=data.get('role', 'staff')
        )
        
        return ResponseHandler.created(
            user.to_dict(),
            "User registered successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Registration failed: {str(e)}", 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    Request body: {
        "id_token": "firebase_id_token"
    }
    """
    try:
        data = request.get_json()
        
        if 'id_token' not in data:
            return ResponseHandler.bad_request("id_token is required")
        
        user = auth_service.login_user(data['id_token'])
        
        if not user:
            return ResponseHandler.unauthorized(
                "Invalid credentials or user not registered"
            )
        
        return ResponseHandler.success(
            user.to_dict(),
            "Login successful"
        )
    
    except ValueError as e:
        return ResponseHandler.forbidden(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Login failed: {str(e)}", 500)


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current logged-in user details"""
    try:
        user = g.current_user
        return ResponseHandler.success(
            user.to_dict(),
            "User details retrieved successfully"
        )
    except Exception as e:
        return ResponseHandler.error(f"Failed to get user details: {str(e)}", 500)


@auth_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@role_required('admin')
def update_user_role(user_id):
    """
    Update user role (admin only)
    Request body: {
        "role": "manager"
    }
    """
    try:
        data = request.get_json()
        
        if 'role' not in data:
            return ResponseHandler.bad_request("role is required")
        
        user = auth_service.update_user_role(user_id, data['role'])
        
        if not user:
            return ResponseHandler.not_found("User not found")
        
        return ResponseHandler.success(
            user.to_dict(),
            "User role updated successfully"
        )
    
    except ValueError as e:
        return ResponseHandler.bad_request(str(e))
    except Exception as e:
        return ResponseHandler.error(f"Failed to update role: {str(e)}", 500)


@auth_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
@role_required('admin')
def deactivate_user(user_id):
    """Deactivate user account (admin only)"""
    try:
        user = auth_service.deactivate_user(user_id)
        
        if not user:
            return ResponseHandler.not_found("User not found")
        
        return ResponseHandler.success(
            user.to_dict(),
            "User deactivated successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to deactivate user: {str(e)}", 500)


@auth_bp.route('/users/<int:user_id>/activate', methods=['PUT'])
@role_required('admin')
def activate_user(user_id):
    """Activate user account (admin only)"""
    try:
        user = auth_service.activate_user(user_id)
        
        if not user:
            return ResponseHandler.not_found("User not found")
        
        return ResponseHandler.success(
            user.to_dict(),
            "User activated successfully"
        )
    
    except Exception as e:
        return ResponseHandler.error(f"Failed to activate user: {str(e)}", 500)