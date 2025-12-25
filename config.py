import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///momo_orders.db"
    )
    CORS_ORIGINS = ["http://localhost:5173"]


class ProductionConfig(Config):
    if not os.environ.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set in production")
