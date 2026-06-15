from app import db
from app.models.skin_profile import SkinProfile


class SkinProfileRepository:

    @staticmethod
    def find_by_user(user_id: str) -> SkinProfile | None:
        return SkinProfile.query.filter_by(user_id=user_id).first()

    @staticmethod
    def create(profile: SkinProfile) -> SkinProfile:
        db.session.add(profile)
        db.session.commit()
        return profile

    @staticmethod
    def commit() -> None:
        db.session.commit()
