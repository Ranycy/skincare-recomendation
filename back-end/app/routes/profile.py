from flask import Blueprint, request, jsonify

from app.controllers.profile_controller import (
    get_preferences,
    get_skin_profile,
    update_preferences,
    upsert_skin_profile,
)

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


@profile_bp.route("/profile/preferences", methods=["GET"])
def preferences():
    result, status = get_preferences(request.headers.get("Authorization", ""))
    return jsonify(result), status


@profile_bp.route("/profile/preferences", methods=["PUT"])
def update_profile_preferences():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = update_preferences(request.headers.get("Authorization", ""), data)
    return jsonify(result), status
