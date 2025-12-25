from flask import Flask
from flask_cors import CORS
import os
import sys
from config import DevelopmentConfig, ProductionConfig

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from models import db
from config import Config
from routes import public_bp, admin_bp
from seed_data import seed_database

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)


    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        # app.config.from_object(Config)
        app.config.from_object(DevelopmentConfig)

    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    
    # Initialize database
    with app.app_context():
        db.create_all()
        
        # Seed database if empty
        from models import MenuItem
        if MenuItem.query.count() == 0:
            seed_database()
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

