from flask import Flask
from flask_cors import CORS
import os
import sys
from config import DevelopmentConfig, ProductionConfig

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from config import Config
from models import db
from routes import public_bp, admin_bp
from seed_data import seed_database

def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    # REGISTER BLUEPRINTS FIRST
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # APPLY CORS AFTER ROUTES EXIST
    CORS(
        app,
        resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PATCH", "OPTIONS"]
    )

    with app.app_context():
        db.create_all()
        from models import MenuItem
        if MenuItem.query.count() == 0:
            seed_database()

    return app

app = create_app()

