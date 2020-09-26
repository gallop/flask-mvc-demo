# coding: utf-8

from app.models.Base import Base, db, MixinJSONSerializer


class Permission(Base, MixinJSONSerializer):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    permission = db.Column(db.String(63))
    add_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    deleted = db.Column(db.Integer, server_default=db.FetchedValue())
