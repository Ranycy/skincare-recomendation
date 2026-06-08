from app import db
from app.controllers.auth_controller import get_user_from_token
from app.models.user import User
from app.models.questionnaire import QuestionnaireProfile
from app.models.recommendation import Recommendation
from app.services.guidance_service import (
    build_explanation_factors,
    build_dynamic_why_recommended,
    build_routine_summary,
    build_weather_insights,
)
from app.services.weather_service import fetch_weather
from datetime import datetime, timezone

_recommender = None

VALID_CATEGORIES = {"moisturizer", "cleanser", "face mask", "eye cream", "sunscreen"}
VALID_SKIN_TYPES = {"normal", "dry", "oily", "combination", "sensitive"}


def get_recommender():
    global _recommender
    if _recommender is None:
        from services.recommender import SkincareRecommender
        _recommender = SkincareRecommender()
    return _recommender


def is_expired(expires_at) -> bool:
    if not expires_at:
        return True

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    return expires_at <= datetime.now(timezone.utc)


def create_recommendation(data: dict, auth_header: str = "") -> tuple[dict, int]:
    questionnaire = data.get("questionnaire", {})
    location = data.get("location", {})
    user_id = data.get("user_id")
    session_token = data.get("session_token")

    product_category = questionnaire.get("product_category", "").lower()
    skin_type = questionnaire.get("skin_type", "").lower()
    skin_concerns = questionnaire.get("skin_concerns", [])
    activity_type = questionnaire.get("activity_type")
    avoided_ingredients = questionnaire.get("avoided_ingredients", [])

    lat = location.get("lat")
    lon = location.get("lon")
    location_method = location.get("method")

    if not product_category or product_category not in VALID_CATEGORIES:
        return {"error": f"Invalid product_category. Must be one of: {', '.join(VALID_CATEGORIES)}"}, 400
    if not skin_type or skin_type not in VALID_SKIN_TYPES:
        return {"error": f"Invalid skin_type. Must be one of: {', '.join(VALID_SKIN_TYPES)}"}, 400
    if lat is None or lon is None:
        return {"error": "Location (lat, lon) is required"}, 400

    user = None
    is_guest = True

    if auth_header:
        user, auth_error = get_user_from_token(auth_header)
        if auth_error:
            return {"error": auth_error}, 401
        user_id = user.id
        is_guest = False
    elif session_token:
        user = User.query.filter_by(session_token=session_token).first()
        if not user or is_expired(user.session_expires_at):
            return {"error": "Invalid or expired guest session"}, 401
        user_id = user.id
        is_guest = True
    elif user_id:
        user = User.query.get(user_id)
        if user:
            is_guest = user.is_guest

    try:
        weather_data = fetch_weather(lat, lon)
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}, 502

    activity = activity_type if product_category == "sunscreen" and activity_type else "indoor"

    recommender = get_recommender()
    results = recommender.get_recommendations(
        weather_data=weather_data,
        skin_type=skin_type,
        selected_products=[product_category],
        concerns=skin_concerns,
        activity=activity,
        avoid_ingredients=avoided_ingredients,
    )
    weather_insights = build_weather_insights(weather_data, questionnaire)
    routine_summary = build_routine_summary(questionnaire, weather_data, results)

    profile = QuestionnaireProfile(
        user_id=user_id,
        product_category=product_category,
        skin_type=skin_type,
        skin_concerns=skin_concerns,
        activity_type=activity_type,
        avoided_ingredients=avoided_ingredients,
        lat=lat,
        lon=lon,
        location_method=location_method,
    )
    db.session.add(profile)
    db.session.flush()

    for rank, product in enumerate(results, start=1):
        dynamic_why = build_dynamic_why_recommended(product, questionnaire, weather_data)
        rec = Recommendation(
            questionnaire_id=profile.id,
            product_name=product["product_name"],
            brand=product["brand"],
            category=product["category"],
            skin_types=product["skin_types"],
            active_ingredients=product["active_ingredients"],
            why_recommended=dynamic_why,
            temp_c=weather_data["temperature"],
            humidity=weather_data["humidity"],
            uv_index=weather_data["uv_index"],
            pm2_5=weather_data["pm25"],
            score=product["score"],
            rank=rank,
            is_guest=is_guest,
        )
        db.session.add(rec)

    db.session.commit()

    return {
        "questionnaire_id": profile.id,
        "weather": {
            "location_name": weather_data.get("location_name", "Lokasi saat ini"),
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "uv_index": weather_data["uv_index"],
            "pm25": weather_data["pm25"],
        },
        "recommendations": [
            {
                "rank": i + 1,
                "product_name": p["product_name"],
                "brand": p["brand"],
                "category": p["category"],
                "skin_types": p["skin_types"],
                "active_ingredients": p["active_ingredients"],
                "why_recommended": build_dynamic_why_recommended(p, questionnaire, weather_data),
                "explanation_factors": build_explanation_factors(p, questionnaire, weather_data),
                "score": p["score"],
            }
            for i, p in enumerate(results)
        ],
        "weather_insights": weather_insights,
        "routine_summary": routine_summary,
    }, 200
