import mongoengine
from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

import mongoengine as mg
from user.models import User
from user.extensions import ma, logger
from user.commons.pagination import Pagination
from user.utils.response import format_response


class UserSchema(ma.Schema):
    id = ma.String(dump_only=True)
    password = ma.String(load_only=True, required=True)
    username = ma.String(required=True)
    email = ma.String(default='')
    phone = ma.String(default='')
    # roles = ma.List(required=False)
    avatar = ma.string(default='')
    gender = ma.String(default='')
    weixin = ma.String(default='')
    qq = ma.String(default='')
    birthday = ma.Date(required=False)
    country = ma.String(default='')  # 国家
    city = ma.String(default='')  # 城市
    graduated_school = ma.String(default='')  # 毕业学校
    company = ma.String(default='')  # 就职公司
    title = ma.String(default='')  # 职位


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required]

    def get(self, id):
        schema = UserSchema()
        try:
            user = User.objects.get(id=id)
            return format_response(schema.dump(user), "get user detail success", 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'user is not exist', 404)

    def put(self, id):
        schema = UserSchema(partial=True)
        try:
            user = User.objects.get(id=id)
            user_data = schema.load(request.json)
            user.update(**user_data)
            user.reload()
            return format_response(schema.dump(user), 'user updated', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'user is not exist', 404)

    def delete(self, id):
        try:
            User.objects.get(id=id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'user deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'user is not exist', 404)


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = {"get": [jwt_required]}

    def get(self):
        try:
            schema = UserSchema(many=True)
            query = User.objects.all()
            objs, page = Pagination(query).paginate(schema)
            return format_response(objs, 'get user list success', 200, page=page)
        except Exception as e:
            return format_response(e.args, 'get user list failure', 500)

    def post(self):
        try:
            schema = UserSchema()
            data = schema.load(request.json)
            user = User.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            return format_response(schema.dump(user), 'user created', 201)
        except mongoengine.errors.NotUniqueError:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response('', 'user exists', 400)
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            return format_response('', 'server error', 500)
