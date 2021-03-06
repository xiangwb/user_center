from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from user.extensions import apispec
from user.api.resources import UserResource, UserList, InternalUserResource
from user.api.resources.user import UserSchema

blueprint = Blueprint("api", __name__, url_prefix="/api/v1/user_center")
api = Api(blueprint)

api.add_resource(UserResource, "/users/<string:id>")
api.add_resource(UserList, "/users/")
api.add_resource(InternalUserResource, '/internal/users/<string:id>')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=InternalUserResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
