import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class following Single Responsibility Principle"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database Configuration
    DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_PORT', '3306')
    DB_USER = os.getenv('DATABASE_USER', 'root')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DB_NAME = os.getenv('DATABASE_NAME', 'product_management_db')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    
    # Firebase Configuration
    FIREBASE_CONFIG_PATH = os.getenv('FIREBASE_CONFIG_PATH', 'firebase-config.json')
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}