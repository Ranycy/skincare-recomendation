import sys
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


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

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(recommend_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
