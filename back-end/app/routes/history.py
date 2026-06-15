from flask import Blueprint, request, jsonify

from app.controllers.history_controller import delete_history_item, get_history, get_history_detail

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def history():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    locale = request.args.get("locale")
    result, status = get_history(request.headers.get("Authorization", ""), page, limit, locale)
    return jsonify(result), status


@history_bp.route("/history/<questionnaire_id>", methods=["GET"])
def history_detail(questionnaire_id):
    locale = request.args.get("locale")
    result, status = get_history_detail(request.headers.get("Authorization", ""), questionnaire_id, locale)
    return jsonify(result), status


@history_bp.route("/history/<questionnaire_id>", methods=["DELETE"])
def delete_history(questionnaire_id):
    result, status = delete_history_item(request.headers.get("Authorization", ""), questionnaire_id)
    return jsonify(result), status
