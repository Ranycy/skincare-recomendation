from app import db
from app.models.user import User


class AuthRepository:

    @staticmethod
    def find_by_id(user_id: str) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_registered_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email, is_guest=False).first()

    @staticmethod
    def find_guest(user_id: str, session_token: str) -> User | None:
        return User.query.filter_by(
            id=user_id,
            session_token=session_token,
            is_guest=True,
        ).first()

    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_locale(user: User, locale: str) -> User:
        user.preferred_locale = locale
        db.session.commit()
        return user
