import uuid
from datetime import datetime, timezone
from app import db


class QuestionnaireProfile(db.Model):
    __tablename__ = "questionnaire_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)
    product_category = db.Column(db.String(50), nullable=False)
    skin_type = db.Column(db.String(50), nullable=False)
    skin_concerns = db.Column(db.JSON, nullable=False, default=list)
    activity_type = db.Column(db.String(20), nullable=True)
    avoided_ingredients = db.Column(db.JSON, nullable=False, default=list)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    location_method = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    recommendations = db.relationship("Recommendation", backref="questionnaire", lazy=True)
