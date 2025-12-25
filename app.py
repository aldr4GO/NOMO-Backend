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

    # Add a test route to check CORS headers
    @app.route('/cors-test')
    def cors_test():
        return {"message": "CORS test successful"}

    # Log response headers for every request
    @app.after_request
    def after_request(response):
        print("Response Headers:", dict(response.headers))
        return response
    print("app = Flask(__name__)")

    # env = os.environ.get("FLASK_ENV", "production")
    env = "production"

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    print(f"env={env}")

    db.init_app(app)

    # REGISTER BLUEPRINTS FIRST
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # APPLY CORS AFTER ROUTES EXIST
    CORS(
        app,
        resources={r"/*": {"origins": ["https://nomo-frontend.vercel.app"]}},
        supports_credentials=True
    )
    with app.app_context():
        db.create_all()
        from models import MenuItem
        if MenuItem.query.count() == 0:
            print("seeding database")
            seed_database()

    return app

app = create_app()

