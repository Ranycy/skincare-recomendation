import uuid
from datetime import datetime, timezone
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    is_guest = db.Column(db.Boolean, nullable=False, default=True)
    session_token = db.Column(db.String(255), unique=True, nullable=True)
    session_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    questionnaires = db.relationship("QuestionnaireProfile", backref="user", lazy=True)
