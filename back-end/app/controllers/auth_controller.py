import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from flask import current_app

from app import db
from app.models.user import User


def generate_jwt(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=current_app.config["JWT_EXPIRATION_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_user_from_token(auth_header: str) -> tuple[User | None, str | None]:
    """Extract and validate JWT from Authorization header.
    Returns (user, None) on success or (None, error_message) on failure.
    """
    if not auth_header.startswith("Bearer "):
        return None, "Authorization header required"

    token = auth_header.split(" ", 1)[1]
    payload = decode_jwt(token)
    if not payload:
        return None, "Invalid or expired token"

    user = User.query.get(payload["user_id"])
    if not user:
        return None, "User not found"

    return user, None


def register_user(email: str, password: str, name: str) -> tuple[dict, int]:
    email = email.strip().lower()
    name = name.strip()

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 409

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = User(email=email, password_hash=password_hash, name=name or None, is_guest=False)
    db.session.add(user)
    db.session.commit()

    token = generate_jwt(user.id)
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "token": token,
    }, 201


def login_user(email: str, password: str) -> tuple[dict, int]:
    email = email.strip().lower()

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email, is_guest=False).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return {"error": "Invalid email or password"}, 401

    token = generate_jwt(user.id)
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "token": token,
    }, 200


def create_guest_session() -> tuple[dict, int]:
    session_token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=current_app.config["GUEST_SESSION_HOURS"])

    user = User(is_guest=True, session_token=session_token, session_expires_at=expires_at)
    db.session.add(user)
    db.session.commit()

    return {
        "user_id": user.id,
        "session_token": session_token,
        "expires_at": expires_at.isoformat(),
    }, 201


def get_current_user(auth_header: str) -> tuple[dict, int]:
    user, error = get_user_from_token(auth_header)
    if error:
        status = 404 if error == "User not found" else 401
        return {"error": error}, status

    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "is_guest": user.is_guest,
    }, 200
