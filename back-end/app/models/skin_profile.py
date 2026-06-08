import uuid
from datetime import datetime, timezone
from app import db


class SkinProfile(db.Model):
    __tablename__ = "skin_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True)
    skin_type = db.Column(db.String(50), nullable=False)
    skin_concerns = db.Column(db.JSON, nullable=False, default=list)
    avoided_ingredients = db.Column(db.JSON, nullable=False, default=list)
    default_product_category = db.Column(db.String(50), nullable=True)
    default_activity_type = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
