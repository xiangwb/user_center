"""Default configuration

Use env var to override
"""

import os

ENV = os.environ.get("FLASK_ENV", "production")
DEBUG = ENV == "development"
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASE_URI = os.environ.get("DATABASE_URI")

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND_URL")
DEFAULT_LOG_DIR = os.environ.get("DEFAULT_LOG_DIR", "./logs")
DEFAULT_LOG_FILE = os.environ.get("DEFAULT_LOG_FILE", "default.log")
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
