from app.controllers.auth_controller import get_user_from_token
from app.models.favorite_product import FavoriteProduct
from app.repositories.favorite_repository import FavoriteRepository


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

    favorites = FavoriteRepository.find_by_user(user.id)
    return {"favorites": [serialize_favorite(f) for f in favorites]}, 200


def add_favorite(auth_header: str, data: dict) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    product_name = (data.get("product_name") or "").strip()
    brand = (data.get("brand") or "").strip() or None
    category = (data.get("category") or "").strip() or None

    if not product_name:
        return {"error": "product_name is required"}, 400

    favorite = FavoriteRepository.find_duplicate(user.id, product_name, brand, category)

    if not favorite:
        favorite = FavoriteProduct(
            user_id=user.id,
            product_name=product_name,
            brand=brand,
            category=category,
            score=data.get("score"),
            source_questionnaire_id=data.get("source_questionnaire_id"),
        )
        FavoriteRepository.create(favorite)

    return {"favorite": serialize_favorite(favorite)}, 201


def delete_favorite(auth_header: str, favorite_id: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        return {"error": error}, 401

    favorite = FavoriteRepository.find_by_id_and_user(favorite_id, user.id)
    if not favorite:
        return {"error": "Favorite product not found"}, 404

    FavoriteRepository.delete(favorite)
    return {"message": "Favorite product removed"}, 200
