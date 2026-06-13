import sys
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect, text

db = SQLAlchemy()
migrate = Migrate()


def ensure_lightweight_schema_updates(app):
    """Apply tiny SQLite-safe schema updates for local capstone development."""
    if not app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        return

    inspector = inspect(db.engine)
    if inspector.has_table("users"):
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "preferred_locale" not in user_columns:
            db.session.execute(text("ALTER TABLE users ADD COLUMN preferred_locale VARCHAR(10) DEFAULT 'en'"))
            db.session.execute(text("UPDATE users SET preferred_locale = 'en' WHERE preferred_locale IS NULL"))
            db.session.commit()

    if inspector.has_table("questionnaire_profiles"):
        columns = {column["name"] for column in inspector.get_columns("questionnaire_profiles")}
        if "location_name" not in columns:
            db.session.execute(text("ALTER TABLE questionnaire_profiles ADD COLUMN location_name VARCHAR(120)"))
            db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    ml_path = os.path.abspath(app.config.get("ML_MODEL_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "machine-learning")))
    if ml_path not in sys.path:
        sys.path.insert(0, ml_path)

    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.recommend import recommend_bp
    from app.routes.history import history_bp
    from app.routes.profile import profile_bp
    from app.routes.favorites import favorites_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(recommend_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")
    app.register_blueprint(profile_bp, url_prefix="/api")
    app.register_blueprint(favorites_bp, url_prefix="/api")

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()
        ensure_lightweight_schema_updates(app)

    return app
