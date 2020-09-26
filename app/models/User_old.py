# coding: utf-8
from sqlalchemy import orm, inspect
from werkzeug.security import generate_password_hash

from app.models.Base import Base, db, MixinJSONSerializer


# mixin并不作为任何类的基类，也不关心与什么类一起使用，而是在运行时动态的同其他零散的类一起组合使用。
# 这里使用Mixin,将MixinJSONSerializer 里的内容组合到该类中
class User():
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    # 非持久化字段，用于user关联其角色信息
    roles = []
    # 非持久化字段，用于在current_user中保存权限列表，便于权限控制
    permissions = []

    @property
    def password(self):
        return self.login_pwd

    @password.setter
    def password(self, raw):
        self.login_pwd = generate_password_hash(raw)

    # @orm.reconstructor
    # def __init__(self):
    #     print('temp:', self.to_json())
    #     columns = inspect(self.__class__).columns
    #     print('keys:', columns.keys())
    #     if not self.fields:
    #         all_columns = set(columns.keys())
    #         self.fields = list(all_columns)


