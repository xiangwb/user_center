"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask import jsonify
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from celery import Celery
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from user.commons.apispec import APISpecExt

from user.loggers import Logger
from user.utils.response import format_response

jwt = JWTManager()
ma = Marshmallow()
db = MongoEngine()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
logger = Logger()
limiter = Limiter(key_func=get_remote_address, default_limits=["10000/day, 2000/minute, 1000/second"])


@jwt.unauthorized_loader
def my_unauthorized_loader(e):
    return jsonify(format_response('', 'Missing Authorization Header', 401)), 401


@jwt.invalid_token_loader
def my_invalid_token_loader(e):
    return jsonify(format_response('', "Bad Authorization header. Expected value 'Bearer <JWT>'", 422)), 422


@jwt.expired_token_loader
def my_expired_token_loader(e):
    return jsonify(format_response('', "Token has expired", 401)), 401
