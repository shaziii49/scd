from functools import wraps
from flask import request, jsonify, g
from ..services.auth_service import AuthService


def token_required(f):
    """
    Decorator to protect routes with Firebase authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token format. Use: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Authentication token is missing'
            }), 401
        
        # Verify token
        auth_service = AuthService()
        decoded_token = auth_service.verify_token(token)
        
        if not decoded_token:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        # Get user from database
        firebase_uid = decoded_token.get('uid')
        user = auth_service.get_user_by_firebase_uid(firebase_uid)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'User account is deactivated'
            }), 403
        
        # Store user in Flask's g object for access in route
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(*roles):
    """
    Decorator to check if user has required role
    Usage: @role_required('admin', 'manager')
    """
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated_function(*args, **kwargs):
            user = g.current_user
            
            if user.role not in roles:
                return jsonify({
                    'success': False,
                    'message': f'Access denied. Required role: {", ".join(roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator