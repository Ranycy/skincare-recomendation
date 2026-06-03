from datetime import datetime, timezone
from flask import current_app

from app import db
from app.controllers.recommend_controller import get_recommender


def get_system_status() -> dict:
    model_loaded = False
    product_count = 0
    try:
        r = get_recommender()
        product_count = len(r.products)
        model_loaded = product_count > 0
    except Exception:
        pass

    db_ok = False
    db_status = "error"
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
        db_status = "connected"
    except Exception as e:
        db_status = str(e)[:40]

    weather_key = bool(current_app.config.get("WEATHERAPI_KEY"))
    ml_path = current_app.config.get("ML_MODEL_PATH", "not set")
    server_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "model_loaded": model_loaded,
        "product_count": product_count,
        "db_ok": db_ok,
        "db_status": db_status,
        "weather_key": weather_key,
        "ml_path": ml_path,
        "server_time": server_time,
    }


def get_status_json() -> tuple[dict, int]:
    status = get_system_status()
    return {
        "status": "ok" if (status["model_loaded"] and status["db_ok"]) else "degraded",
        "model_loaded": status["model_loaded"],
        "product_count": status["product_count"],
        "database": status["db_ok"],
        "weather_api_configured": status["weather_key"],
        "ml_model_path": status["ml_path"],
        "server_time": datetime.now(timezone.utc).isoformat(),
    }, 200
