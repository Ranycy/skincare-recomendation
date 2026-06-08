from app import db
from app.controllers.auth_controller import get_user_from_token
from app.models.favorite_product import FavoriteProduct


def serialize_favorite(favorite: FavoriteProduct) -> dict:
    return {
        "id": favorite.id,
        "product_name": favorite.product_name,
        "brand": favorite.brand,
        "category": favorite.category,
        "score": favorite.score,
        "source_questionnaire_id": favorite.source_questionnaire_id,
        "created_at": favorite.created_at.isoformat(),
    }


def get_favorites(auth_header: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    favorites = (
        FavoriteProduct.query
        .filter_by(user_id=user.id)
        .order_by(FavoriteProduct.created_at.desc())
        .all()
    )

    return {"favorites": [serialize_favorite(favorite) for favorite in favorites]}, 200


def add_favorite(auth_header: str, data: dict) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    product_name = (data.get("product_name") or "").strip()
    brand = (data.get("brand") or "").strip() or None
    category = (data.get("category") or "").strip() or None

    if not product_name:
        return {"error": "product_name is required"}, 400

    favorite = FavoriteProduct.query.filter_by(
        user_id=user.id,
        product_name=product_name,
        brand=brand,
        category=category,
    ).first()

    if not favorite:
        favorite = FavoriteProduct(
            user_id=user.id,
            product_name=product_name,
            brand=brand,
            category=category,
            score=data.get("score"),
            source_questionnaire_id=data.get("source_questionnaire_id"),
        )
        db.session.add(favorite)
        db.session.commit()

    return {"favorite": serialize_favorite(favorite)}, 201


def delete_favorite(auth_header: str, favorite_id: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    favorite = FavoriteProduct.query.filter_by(id=favorite_id, user_id=user.id).first()
    if not favorite:
        return {"error": "Favorite product not found"}, 404

    db.session.delete(favorite)
    db.session.commit()
    return {"message": "Favorite product removed"}, 200
