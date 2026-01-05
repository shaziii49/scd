from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import config_by_name
import os

# Initialize extensions
db = SQLAlchemy()


def create_app(config_name=None):
    """
    Application Factory Pattern
    Creates and configures the Flask application
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # IMPORTANT: Specify template and static folders relative to project root
    app = Flask(__name__)

    app.template_folder = os.path.join(os.getcwd(), 'FlaskProjectSCD', 'templates')
    app.static_folder = os.path.join(os.getcwd(), 'FlaskProjectSCD', 'static')

    # Recreate jinja environment with new template folder
    app.jinja_env = app.create_jinja_environment()

    # Load configuration
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from .controllers.supplier_controller import supplier_bp

    app.register_blueprint(supplier_bp)
    
    # Add simple web route for home page
    from flask import render_template
    
    @app.route('/')
    def index():
        """Home page - show suppliers"""
        return render_template('suppliers.html')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'success': False, 'message': 'Internal server error'}, 500

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'success': True, 'message': 'Server is running'}, 200

    return app