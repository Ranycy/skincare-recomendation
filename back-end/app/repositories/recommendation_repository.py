from app import db
from app.models.recommendation import Recommendation


class RecommendationRepository:

    @staticmethod
    def find_by_questionnaire(questionnaire_id: str) -> list[Recommendation]:
        return (
            Recommendation.query
            .filter_by(questionnaire_id=questionnaire_id)
            .order_by(Recommendation.rank)
            .all()
        )

    @staticmethod
    def create(rec: Recommendation) -> Recommendation:
        db.session.add(rec)
        return rec

    @staticmethod
    def delete_by_questionnaire(questionnaire_id: str) -> None:
        Recommendation.query.filter_by(questionnaire_id=questionnaire_id).delete()

    @staticmethod
    def commit() -> None:
        db.session.commit()
