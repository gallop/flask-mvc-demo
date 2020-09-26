# coding: utf-8
from werkzeug.security import generate_password_hash
from app.models.Base import Base, db, MixinJSONSerializer


class Role(Base, MixinJSONSerializer):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False, unique=True)
    desc = db.Column(db.String(1023))
    enabled = db.Column(db.Integer, server_default=db.FetchedValue())
    add_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    deleted = db.Column(db.Integer, server_default=db.FetchedValue())
