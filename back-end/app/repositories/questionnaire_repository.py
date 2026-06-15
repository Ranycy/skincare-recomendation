from app import db
from app.models.questionnaire import QuestionnaireProfile


class QuestionnaireRepository:

    @staticmethod
    def find_by_id(questionnaire_id: str) -> QuestionnaireProfile | None:
        return db.session.get(QuestionnaireProfile, questionnaire_id)

    @staticmethod
    def find_by_id_and_user(questionnaire_id: str, user_id: str) -> QuestionnaireProfile | None:
        return QuestionnaireProfile.query.filter_by(
            id=questionnaire_id,
            user_id=user_id,
        ).first()

    @staticmethod
    def find_by_user_paginated(user_id: str, page: int, limit: int) -> tuple[list[QuestionnaireProfile], int]:
        query = QuestionnaireProfile.query.filter_by(user_id=user_id)
        total = query.count()
        profiles = (
            query
            .order_by(QuestionnaireProfile.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return profiles, total

    @staticmethod
    def create(profile: QuestionnaireProfile) -> QuestionnaireProfile:
        db.session.add(profile)
        db.session.flush()
        return profile

    @staticmethod
    def delete(profile: QuestionnaireProfile) -> None:
        db.session.delete(profile)
        db.session.commit()
