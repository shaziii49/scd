from flask import jsonify
from typing import Any, Optional, Dict


class ResponseHandler:
    """
    Standardized response handler for API responses
    Follows Single Responsibility Principle
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", 
                status_code: int = 200, **kwargs) -> tuple:
        """Return success response"""
        response = {
            'success': True,
            'message': message,
        }
        
        if data is not None:
            response['data'] = data
        
        # Add any additional fields
        response.update(kwargs)
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400, 
              errors: Optional[Dict] = None) -> tuple:
        """Return error response"""
        response = {
            'success': False,
            'message': message
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), status_code
    
    @staticmethod
    def created(data: Any, message: str = "Resource created successfully") -> tuple:
        """Return created response (201)"""
        return ResponseHandler.success(data, message, 201)
    
    @staticmethod
    def not_found(message: str = "Resource not found") -> tuple:
        """Return not found response (404)"""
        return ResponseHandler.error(message, 404)
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized access") -> tuple:
        """Return unauthorized response (401)"""
        return ResponseHandler.error(message, 401)
    
    @staticmethod
    def forbidden(message: str = "Access forbidden") -> tuple:
        """Return forbidden response (403)"""
        return ResponseHandler.error(message, 403)
    
    @staticmethod
    def bad_request(message: str = "Bad request", errors: Optional[Dict] = None) -> tuple:
        """Return bad request response (400)"""
        return ResponseHandler.error(message, 400, errors)
    
    @staticmethod
    def paginated(items: list, total: int, page: int, per_page: int, 
                  message: str = "Success") -> tuple:
        """Return paginated response"""
        total_pages = (total + per_page - 1) // per_page  # Ceiling division
        
        return ResponseHandler.success(
            data=items,
            message=message,
            pagination={
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        )