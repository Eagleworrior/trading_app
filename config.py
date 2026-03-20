import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "trading.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SIMULATOR_TICK_SECONDS = float(os.environ.get("SIMULATOR_TICK_SECONDS", "1.0"))

