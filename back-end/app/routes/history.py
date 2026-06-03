from flask import Blueprint, request, jsonify

from app.controllers.history_controller import get_history

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def history():
    result, status = get_history(request.headers.get("Authorization", ""))
    return jsonify(result), status
