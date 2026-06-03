import uuid
from datetime import datetime, timezone
from app import db


class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    questionnaire_id = db.Column(db.String(36), db.ForeignKey("questionnaire_profiles.id"), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50))
    skin_types = db.Column(db.JSON)
    active_ingredients = db.Column(db.JSON)
    why_recommended = db.Column(db.Text)
    temp_c = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    uv_index = db.Column(db.Float)
    pm2_5 = db.Column(db.Float)
    score = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    is_guest = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
