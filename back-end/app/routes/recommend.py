from flask import Blueprint, request, jsonify

from app.controllers.recommend_controller import create_recommendation

recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = create_recommendation(data)
    return jsonify(result), status
