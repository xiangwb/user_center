from flask import request, jsonify, Blueprint, current_app as app, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

from user.auth.helpers import revoke_token, is_token_revoked, add_token_to_database
from user.extensions import pwd_context, jwt, apispec
from user.loggers import get_logger
from user.models import User
from user.utils.response import format_response

logger = get_logger('user', 'user')

blueprint = Blueprint("auth", __name__, url_prefix="/api/v1/user_center")


@blueprint.route("/login/", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - auth
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: myuser
                  required: true
                password:
                  type: string
                  example: P4$$w0rd!
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
                  refresh_token:
                    type: string
                    example: myrefreshtoken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        # return jsonify({"msg": "Missing JSON in request"}), 400
        return jsonify(format_response('', 'Missing JSON in request', 400))

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        # return jsonify({"msg": "Missing username or password"}), 400
        return jsonify(format_response('', 'Missing username or password', 400))

    user = User.objects.filter(username=username).first()
    logger.debug("user:{}".format(user))
    if user is None or not pwd_context.verify(password, user.password):
        # return jsonify({"msg": "Bad credentials"}), 400
        return jsonify(format_response('', 'Bad credentials', 400))

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    # return jsonify(ret), 200
    return jsonify(format_response(ret, 'login success', 200))


@blueprint.route("/refresh/", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - auth
      parameters:
        - in: header
          name: Authorization
          required: true
          description: valid refresh token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(format_response(ret, 'refresh access token success', 200))


@blueprint.route("/revoke_access/", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    # return jsonify({"message": "token revoked"}), 200
    return jsonify(format_response('', 'revoke access token success', 200))


@blueprint.route("/revoke_refresh/", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    # return jsonify({"message": "token revoked"}), 200
    return jsonify(format_response('', 'revoke refresh token success', 200))


@blueprint.route("/auth/", methods=["GET"])
@jwt_required
def auth():
    """auth for api gateway

    ---
    get:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        400:
          description: bad request
        401:
          description: unauthorized
    """
    # return jsonify({"message": "token revoked"}), 200
    user_id = get_jwt_identity()
    resp = make_response(jsonify(format_response('', 'auth success', 200), 200))
    resp.headers.extend({"X-Auth-User-Id": user_id})
    return resp


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.objects.get(id=identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
