import uuid
from datetime import datetime, timezone
from app import db


class FavoriteProduct(db.Model):
    __tablename__ = "favorite_products"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Float, nullable=True)
    source_questionnaire_id = db.Column(db.String(36), db.ForeignKey("questionnaire_profiles.id"), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
