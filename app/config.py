import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "sigr-linea-base-desarrollo")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    default_db = "sqlite:///" + os.path.join(INSTANCE_DIR, "sigr.db").replace("\\", "/")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default_db)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "testing-sigr"
