#!/usr/bin/env python3
"""
Application entry point for Supplier Management System
"""
import os
from FlaskProjectSCD.app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
