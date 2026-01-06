from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def healthcheck():
    return (
        jsonify({"status": "ok", "message": "Apple Health backend server is running."}),
        200,
    )
