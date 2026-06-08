from app import db
from app.controllers.auth_controller import get_user_from_token
from app.models.favorite_product import FavoriteProduct
from app.models.questionnaire import QuestionnaireProfile
from app.models.recommendation import Recommendation
from app.services.guidance_service import (
    build_explanation_factors,
    build_routine_summary,
    build_weather_insights,
)


def rec_to_product(rec: Recommendation) -> dict:
    return {
        "rank": rec.rank,
        "product_name": rec.product_name,
        "brand": rec.brand,
        "category": rec.category,
        "skin_types": rec.skin_types,
        "active_ingredients": rec.active_ingredients,
        "why_recommended": rec.why_recommended,
        "score": rec.score,
    }


def profile_to_history_item(profile: QuestionnaireProfile, include_recommendations: bool = True) -> dict:
    recs = (
        Recommendation.query
        .filter_by(questionnaire_id=profile.id)
        .order_by(Recommendation.rank)
        .all()
    )
    weather = {
        "location_name": "Lokasi saat ini",
        "temperature": recs[0].temp_c if recs else None,
        "humidity": recs[0].humidity if recs else None,
        "uv_index": recs[0].uv_index if recs else None,
        "pm25": recs[0].pm2_5 if recs else None,
    }
    questionnaire = {
        "product_category": profile.product_category,
        "skin_type": profile.skin_type,
        "skin_concerns": profile.skin_concerns,
        "activity_type": profile.activity_type,
        "avoided_ingredients": profile.avoided_ingredients,
    }
    products = [rec_to_product(rec) for rec in recs]
    recommendations = [
        {
            **product,
            "explanation_factors": build_explanation_factors(product, questionnaire, weather),
        }
        for product in products
    ]

    item = {
        "questionnaire_id": profile.id,
        "product_category": profile.product_category,
        "skin_type": profile.skin_type,
        "skin_concerns": profile.skin_concerns,
        "activity_type": profile.activity_type,
        "avoided_ingredients": profile.avoided_ingredients,
        "location": {
            "lat": profile.lat,
            "lon": profile.lon,
            "method": profile.location_method,
        },
        "created_at": profile.created_at.isoformat(),
        "weather": weather,
        "weather_insights": build_weather_insights(weather, questionnaire),
        "routine_summary": build_routine_summary(questionnaire, weather, products),
        "top_recommendation": recommendations[0] if recommendations else None,
    }

    if include_recommendations:
        item["recommendations"] = recommendations

    return item


def get_history(auth_header: str, page: int = 1, limit: int = 10) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    page = max(page, 1)
    limit = min(max(limit, 1), 50)
    query = QuestionnaireProfile.query.filter_by(user_id=user.id)
    total = query.count()
    profiles = (
        query
        .order_by(QuestionnaireProfile.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    history = [profile_to_history_item(profile, include_recommendations=False) for profile in profiles]

    return {
        "history": history,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
    }, 200


def get_history_detail(auth_header: str, questionnaire_id: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    profile = QuestionnaireProfile.query.filter_by(id=questionnaire_id, user_id=user.id).first()
    if not profile:
        return {"error": "History item not found"}, 404

    return {"history_item": profile_to_history_item(profile)}, 200


def delete_history_item(auth_header: str, questionnaire_id: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    profile = QuestionnaireProfile.query.filter_by(id=questionnaire_id, user_id=user.id).first()
    if not profile:
        return {"error": "History item not found"}, 404

    FavoriteProduct.query.filter_by(
        user_id=user.id,
        source_questionnaire_id=questionnaire_id,
    ).update({"source_questionnaire_id": None})
    Recommendation.query.filter_by(questionnaire_id=questionnaire_id).delete()
    db.session.delete(profile)
    db.session.commit()

    return {"message": "History item deleted"}, 200
