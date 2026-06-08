from flask import Blueprint, request, jsonify

from app.controllers.profile_controller import get_skin_profile, upsert_skin_profile

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/skin", methods=["GET"])
def skin_profile():
    result, status = get_skin_profile(request.headers.get("Authorization", ""))
    return jsonify(result), status


@profile_bp.route("/profile/skin", methods=["PUT"])
def update_skin_profile():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = upsert_skin_profile(request.headers.get("Authorization", ""), data)
    return jsonify(result), status
