from user.extensions import pwd_context
from user.models.mongo import CommonDocument, SearchableMixin
import mongoengine as mongo


class User(CommonDocument, SearchableMixin):
    """Basic user model
    """
    # 基础字段
    username = mongo.StringField(required=True, max_length=100, unique=True)
    email = mongo.StringField(required=False, max_length=80)
    password = mongo.StringField(required=True, max_length=255)
    active = mongo.BooleanField(default=True)
    phone = mongo.StringField(max_length=16, unique=True, required=False)
    roles = mongo.ListField()
    gender = mongo.StringField(choices=['F', 'M', ''], default='')
    wechat = mongo.StringField(default='', max_length=64)
    qq = mongo.StringField(default='', max_length=64)
    birthday = mongo.DateField(required=False)
    country = mongo.StringField(required=False, max_length=128)  # 国家
    city = mongo.StringField(required=False, max_length=128)  # 城市
    graduated_school = mongo.StringField(required=False, max_length=128)  # 毕业学校
    company = mongo.StringField(required=False, max_length=128)  # 就职公司
    title = mongo.StringField(required=False, max_length=64)  # 职位

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    # 扩展字段

    def clean(self, **kwargs):
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username
