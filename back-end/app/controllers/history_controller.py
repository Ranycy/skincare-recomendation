from app.controllers.auth_controller import get_user_from_token
from app.models.questionnaire import QuestionnaireProfile
from app.models.recommendation import Recommendation


def get_history(auth_header: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    profiles = (
        QuestionnaireProfile.query
        .filter_by(user_id=user.id)
        .order_by(QuestionnaireProfile.created_at.desc())
        .all()
    )

    history = []
    for profile in profiles:
        recs = (
            Recommendation.query
            .filter_by(questionnaire_id=profile.id)
            .order_by(Recommendation.rank)
            .all()
        )

        history.append({
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
            "weather": {
                "temperature": recs[0].temp_c if recs else None,
                "humidity": recs[0].humidity if recs else None,
                "uv_index": recs[0].uv_index if recs else None,
                "pm25": recs[0].pm2_5 if recs else None,
            },
            "recommendations": [
                {
                    "rank": rec.rank,
                    "product_name": rec.product_name,
                    "brand": rec.brand,
                    "category": rec.category,
                    "skin_types": rec.skin_types,
                    "active_ingredients": rec.active_ingredients,
                    "why_recommended": rec.why_recommended,
                    "score": rec.score,
                }
                for rec in recs
            ],
        })

    return {"history": history}, 200
