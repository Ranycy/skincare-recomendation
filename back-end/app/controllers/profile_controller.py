from app import db
from app.controllers.auth_controller import get_user_from_token
from app.models.skin_profile import SkinProfile

VALID_CATEGORIES = {"moisturizer", "cleanser", "face mask", "eye cream", "sunscreen"}
VALID_SKIN_TYPES = {"normal", "dry", "oily", "combination", "sensitive"}
VALID_ACTIVITIES = {"indoor", "outdoor", None, ""}


def serialize_skin_profile(profile: SkinProfile | None) -> dict | None:
    if not profile:
        return None

    return {
        "id": profile.id,
        "skin_type": profile.skin_type,
        "skin_concerns": profile.skin_concerns or [],
        "avoided_ingredients": profile.avoided_ingredients or [],
        "default_product_category": profile.default_product_category,
        "default_activity_type": profile.default_activity_type,
        "created_at": profile.created_at.isoformat(),
        "updated_at": profile.updated_at.isoformat(),
    }


def get_skin_profile(auth_header: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    profile = SkinProfile.query.filter_by(user_id=user.id).first()
    return {"profile": serialize_skin_profile(profile)}, 200


def upsert_skin_profile(auth_header: str, data: dict) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    skin_type = (data.get("skin_type") or "").lower()
    product_category = data.get("default_product_category")
    activity_type = data.get("default_activity_type")
    skin_concerns = data.get("skin_concerns") or []
    avoided_ingredients = data.get("avoided_ingredients") or []

    if skin_type not in VALID_SKIN_TYPES:
        return {"error": f"Invalid skin_type. Must be one of: {', '.join(VALID_SKIN_TYPES)}"}, 400

    if product_category and product_category not in VALID_CATEGORIES:
        return {"error": f"Invalid default_product_category. Must be one of: {', '.join(VALID_CATEGORIES)}"}, 400

    if activity_type not in VALID_ACTIVITIES:
        return {"error": "Invalid default_activity_type. Must be indoor or outdoor"}, 400

    profile = SkinProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = SkinProfile(user_id=user.id, skin_type=skin_type)
        db.session.add(profile)

    profile.skin_type = skin_type
    profile.skin_concerns = skin_concerns
    profile.avoided_ingredients = avoided_ingredients
    profile.default_product_category = product_category
    profile.default_activity_type = activity_type or None

    db.session.commit()
    return {"profile": serialize_skin_profile(profile)}, 200
