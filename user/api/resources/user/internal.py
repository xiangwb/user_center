from flask_restful import Resource

import mongoengine as mg
from user.models import User
from user.extensions import ma
from user.utils.response import format_response


class UserSchema(ma.Schema):
    id = ma.String(dump_only=True)
    password = ma.String(load_only=True, required=True)
    username = ma.String(required=True)
    email = ma.String(default='')
    phone = ma.String(default='')
    # roles = ma.List(required=False)
    avatar = ma.String(default='')
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

    def get(self, id):
        schema = UserSchema()
        try:
            user = User.objects.get(id=id)
            return format_response(schema.dump(user), "get user detail success", 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'user is not exist', 404)


