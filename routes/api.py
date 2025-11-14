import os
from flask import Blueprint, request, jsonify, current_app
from models.ai_integration import ai_query_handler, build_all_if_missing

api_bp = Blueprint("api", __name__)

@api_bp.before_app_request
def prepare():
    skip = os.environ.get("NEPTUNE_SKIP_BUILD")
    if current_app and current_app.config.get("TESTING"):
        skip = "1"
    if skip:
        if not getattr(api_bp, "_prepared", False):
            api_bp._prepared = True
        return

    if not getattr(api_bp, "_prepared", False):
        build_all_if_missing()
        api_bp._prepared = True


@api_bp.route("/chat", methods=["POST"])
def chat():
    try:
        payload = request.get_json(force=True)
        query = payload.get("query", "")
        context = payload.get("context_data", {})
        result = ai_query_handler(query, context)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
