from user.models.mongo import CommonDocument, SearchableMixin
import mongoengine as mongo


# 先预留，暂不实现
class Permission(CommonDocument, SearchableMixin):
    """Basic permission model
    """
    # 基础字段
    name = mongo.StringField(required=True, max_length=100, unique=True)

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def __repr__(self):
        return "<Permission %s>" % self.name
