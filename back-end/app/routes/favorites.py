from flask import Blueprint, request, jsonify

from app.controllers.favorite_controller import add_favorite, delete_favorite, get_favorites

favorites_bp = Blueprint("favorites", __name__)


@favorites_bp.route("/favorites", methods=["GET"])
def favorites():
    result, status = get_favorites(request.headers.get("Authorization", ""))
    return jsonify(result), status


@favorites_bp.route("/favorites", methods=["POST"])
def create_favorite():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = add_favorite(request.headers.get("Authorization", ""), data)
    return jsonify(result), status


@favorites_bp.route("/favorites/<favorite_id>", methods=["DELETE"])
def remove_favorite(favorite_id):
    result, status = delete_favorite(request.headers.get("Authorization", ""), favorite_id)
    return jsonify(result), status
