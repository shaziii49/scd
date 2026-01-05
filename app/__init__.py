from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate('firebase-config.json')
        firebase_admin.initialize_app(cred)

    # Import models to ensure they are registered with SQLAlchemy
    from app import models

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Simple route
    @app.route('/')
    def hello():
        return 'Hello, Flask!'

    return app