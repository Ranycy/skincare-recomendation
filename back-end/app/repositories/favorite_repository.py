from app import db
from app.models.favorite_product import FavoriteProduct


class FavoriteRepository:

    @staticmethod
    def find_by_user(user_id: str) -> list[FavoriteProduct]:
        return (
            FavoriteProduct.query
            .filter_by(user_id=user_id)
            .order_by(FavoriteProduct.created_at.desc())
            .all()
        )

    @staticmethod
    def find_by_id_and_user(favorite_id: str, user_id: str) -> FavoriteProduct | None:
        return FavoriteProduct.query.filter_by(id=favorite_id, user_id=user_id).first()

    @staticmethod
    def find_duplicate(user_id: str, product_name: str, brand: str | None, category: str | None) -> FavoriteProduct | None:
        return FavoriteProduct.query.filter_by(
            user_id=user_id,
            product_name=product_name,
            brand=brand,
            category=category,
        ).first()

    @staticmethod
    def create(favorite: FavoriteProduct) -> FavoriteProduct:
        db.session.add(favorite)
        db.session.commit()
        return favorite

    @staticmethod
    def delete(favorite: FavoriteProduct) -> None:
        db.session.delete(favorite)
        db.session.commit()

    @staticmethod
    def clear_questionnaire_link(user_id: str, questionnaire_id: str) -> None:
        FavoriteProduct.query.filter_by(
            user_id=user_id,
            source_questionnaire_id=questionnaire_id,
        ).update({"source_questionnaire_id": None})
