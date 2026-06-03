from flask import Blueprint, request, jsonify

from app.controllers.auth_controller import (
    register_user,
    login_user,
    create_guest_session,
    get_current_user,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = register_user(
        email=data.get("email", ""),
        password=data.get("password", ""),
        name=data.get("name", ""),
    )
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    result, status = login_user(
        email=data.get("email", ""),
        password=data.get("password", ""),
    )
    return jsonify(result), status


@auth_bp.route("/guest", methods=["POST"])
def guest_session():
    result, status = create_guest_session()
    return jsonify(result), status


@auth_bp.route("/me", methods=["GET"])
def me():
    result, status = get_current_user(request.headers.get("Authorization", ""))
    return jsonify(result), status
