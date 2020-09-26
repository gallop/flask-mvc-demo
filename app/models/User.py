# coding: utf-8
from werkzeug.security import generate_password_hash
from app.models.Base import Base, db, MixinJSONSerializer


class User(Base, MixinJSONSerializer):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True, info='??uid')
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='???')
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='????')
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='????')
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1?? 2?? 0????')
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue(), info='??')
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue(), info='?????')
    login_pwd = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue(), info='????')
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='???????????')
    role_ids = db.Column(db.String(255))
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1??? 0???')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='????????')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='????')

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