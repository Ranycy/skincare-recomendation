import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///skinsense.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")
    ML_MODEL_PATH = os.getenv("ML_MODEL_PATH", os.path.abspath(os.path.join(BASE_DIR, "..", "machine-learning")))
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    GUEST_SESSION_HOURS = int(os.getenv("GUEST_SESSION_HOURS", "24"))
